from pathlib import Path
import io

import pandas as pd
import joblib

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException,
    Depends
)

from auth.dependencies import get_current_admin
from services.behavior_analysis import analyze_behavior
from services.recommendation_engine import recommend

router = APIRouter(
    prefix="/api",
    tags=["Prediction"]
)

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = (
    BASE_DIR
    / "ml_models"
    / "churn_model.pkl"
)

model_data = joblib.load(MODEL_PATH)

churn_model = model_data["pipeline"]

FEATURE_COLUMNS = model_data["feature_columns"]

print("Churn model loaded successfully.")
print("Expected features:")
print(FEATURE_COLUMNS)

@router.post("/predict")
async def predict(
    file: UploadFile = File(...),
    _: dict = Depends(get_current_admin)
):

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file provided."
        )

    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Only CSV files are currently supported."
        )

    try:
        contents = await file.read()

        df = pd.read_csv(
            io.BytesIO(contents)
        )

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Could not read CSV: {str(e)}"
        )

    if df.empty:
        raise HTTPException(
            status_code=400,
            detail="Uploaded CSV contains no rows."
        )

    missing_columns = [
        column
        for column in FEATURE_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Uploaded CSV is missing required columns.",
                "missing_columns": missing_columns,
                "required_columns": FEATURE_COLUMNS
            }
        )

    X = df[FEATURE_COLUMNS].copy()

    try:
        churn_predictions = churn_model.predict(X)

        churn_probabilities = (
            churn_model.predict_proba(X)[:, 1]
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Churn prediction failed: {str(e)}"
        )

    # the dashboard result

    results = []

    for i in range(len(df)):

        customer = df.iloc[i].to_dict()

        churn_prediction = int(
            churn_predictions[i]
        )

        churn_probability = float(
            churn_probabilities[i]
        )

        behavior = analyze_behavior(customer)

        recommendation = recommend(
            churn_probability,
            behavior
        )

        if "Phone Number" in df.columns:
            customer_id = df.iloc[i]["Phone Number"]

        elif "customerID" in df.columns:
            customer_id = df.iloc[i]["customerID"]

        elif "customer_id" in df.columns:
            customer_id = df.iloc[i]["customer_id"]

        else:
            customer_id = i

        results.append({
            "customer_id": str(customer_id),
            "churn_prediction": churn_prediction,
            "churn_score": round(
                churn_probability,
                4
            ),
            "behavior": behavior,
            "recommendation": recommendation
        })

    total = len(results)

    high_churn_count = sum(
        result["churn_score"] >= 0.70
        for result in results
    )

    upsell_count = sum(
        result["recommendation"]["recommendation_type"]
        == "UPSELL"
        for result in results
    )

    retention_count = sum(
        result["recommendation"]["recommendation_type"]
        == "RETENTION"
        for result in results
    )

    no_recommendation_count = sum(
        result["recommendation"]["recommendation_type"]
        == "NONE"
        for result in results
    )

    return {
        "success": True,
        "filename": file.filename,
        "total": total,
        "results": results,
        "summary": {
            "total": total,
            "high_churn_count": high_churn_count,
            "high_churn_percentage": round(
                high_churn_count / total * 100,
                2
            ),
            "upsell_count": upsell_count,
            "retention_count": retention_count,
            "no_recommendation_count":
                no_recommendation_count
        }
    }