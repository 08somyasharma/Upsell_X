from pathlib import Path

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import pandas as pd
import joblib
import io

from services.behavior_analysis import analyze_behavior
from services.recommendation_engine import recommend


# =========================================================
# APP
# =========================================================

app = FastAPI(
    title="Upsell & Churn Prediction API",
    version="1.0.0"
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = (
    BASE_DIR
    / "ml_models"
    / "churn_model.pkl"
)


# =========================================================
# LOAD CHURN MODEL
# =========================================================

try:

    model_data = joblib.load(MODEL_PATH)

    churn_model = model_data["pipeline"]

    FEATURE_COLUMNS = model_data["feature_columns"]

    print("Churn model loaded successfully.")
    print("Expected features:")
    print(FEATURE_COLUMNS)

except Exception as e:

    print("ERROR loading churn model:")
    print(e)

    churn_model = None
    FEATURE_COLUMNS = []


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
def health():

    return {
        "status": "ok",
        "churn_model_loaded": churn_model is not None,
        "feature_count": len(FEATURE_COLUMNS)
    }


# =========================================================
# PREDICTION
# =========================================================

@app.post("/api/predict")
async def predict(
    file: UploadFile = File(...)
):

    # -----------------------------------------------------
    # Validate file
    # -----------------------------------------------------

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


    # -----------------------------------------------------
    # Check model
    # -----------------------------------------------------

    if churn_model is None:

        raise HTTPException(
            status_code=500,
            detail="Churn model is not loaded."
        )


    # -----------------------------------------------------
    # Read CSV
    # -----------------------------------------------------

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


    # -----------------------------------------------------
    # Validate model columns
    # -----------------------------------------------------

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


    # -----------------------------------------------------
    # Prepare model input
    # -----------------------------------------------------

    X = df[FEATURE_COLUMNS].copy()


    # -----------------------------------------------------
    # Churn prediction
    #
    # The pipeline already contains preprocessing.
    # Do NOT scale/impute manually here.
    # -----------------------------------------------------

    try:

        churn_predictions = (
            churn_model.predict(X)
        )

        churn_probabilities = (
            churn_model.predict_proba(X)[:, 1]
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Churn prediction failed: {str(e)}"
        )


    # =====================================================
    # CUSTOMER RESULTS
    # =====================================================

    results = []

    for i in range(len(df)):

        customer = df.iloc[i].to_dict()

        churn_prediction = int(
            churn_predictions[i]
        )

        churn_probability = float(
            churn_probabilities[i]
        )


        # -------------------------------------------------
        # Behavior analysis
        # -------------------------------------------------

        try:

            behavior = analyze_behavior(
                customer
            )

        except Exception as e:

            raise HTTPException(
                status_code=500,
                detail={
                    "message": "Behavior analysis failed.",
                    "error": str(e)
                }
            )


        # -------------------------------------------------
        # Recommendation
        # -------------------------------------------------

        try:

            recommendation = recommend(
                churn_probability,
                behavior
            )

        except Exception as e:

            raise HTTPException(
                status_code=500,
                detail={
                    "message": "Recommendation engine failed.",
                    "error": str(e)
                }
            )


        # -------------------------------------------------
        # Customer ID
        # -------------------------------------------------

        if "Phone Number" in df.columns:

            customer_id = df.iloc[i]["Phone Number"]

        elif "customerID" in df.columns:

            customer_id = df.iloc[i]["customerID"]

        elif "customer_id" in df.columns:

            customer_id = df.iloc[i]["customer_id"]

        else:

            customer_id = i


        # -------------------------------------------------
        # Final result
        # -------------------------------------------------

        results.append({

            "customer_id":
                str(customer_id),

            "churn_prediction":
                churn_prediction,

            "churn_score":
                round(
                    churn_probability,
                    4
                ),

            "behavior":
                behavior,

            "recommendation":
                recommendation
        })


    # =====================================================
    # SUMMARY
    # =====================================================

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


    summary = {

        "total":
            total,

        "high_churn_count":
            high_churn_count,

        "high_churn_percentage":
            round(
                high_churn_count / total * 100,
                2
            ),

        "upsell_count":
            upsell_count,

        "retention_count":
            retention_count,

        "no_recommendation_count":
            no_recommendation_count
    }


    # =====================================================
    # RESPONSE
    # =====================================================

    return {

        "success": True,

        "filename":
            file.filename,

        "total":
            total,

        "results":
            results,

        "summary":
            summary
    }