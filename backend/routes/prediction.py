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

from services.schema_analyzer import (
    analyze_schema
)

from services.behavior_analysis import (
    analyze_behavior
)

from services.recommendation_engine import (
    recommend
)

from schemas import MessageRequest
from services.message_generator import generate_message


# =========================================================
# ROUTER
# =========================================================

router = APIRouter(
    prefix="/api",
    tags=["Prediction"]
)


# =========================================================
# PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = (
    BASE_DIR
    / "ml_models"
    / "churn_model.pkl"
)


# =========================================================
# LOAD CHURN MODEL
# =========================================================

try:

    model_data = joblib.load(
        MODEL_PATH
    )

    churn_model = model_data[
        "pipeline"
    ]

    FEATURE_COLUMNS = model_data[
        "feature_columns"
    ]

    TRAINING_MEDIANS = model_data[
        "training_medians"
    ]

    print(
        "Churn model loaded successfully."
    )

    print(
        "Expected features:"
    )

    print(
        FEATURE_COLUMNS
    )


except Exception as e:

    print(
        "ERROR loading churn model:"
    )

    print(e)

    churn_model = None

    FEATURE_COLUMNS = []

    TRAINING_MEDIANS = {}


# =========================================================
# PREDICTION
# =========================================================

@router.post("/predict")
async def predict(
    file: UploadFile = File(...),
    _: dict = Depends(get_current_admin)
):

    # -----------------------------------------------------
    # Validate file
    # -----------------------------------------------------

    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail="No file provided."
        )


    if not file.filename.lower().endswith(
        ".csv"
    ):

        raise HTTPException(
            status_code=400,
            detail=(
                "Only CSV files are currently "
                "supported."
            )
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
    # Check training medians
    # -----------------------------------------------------

    if not TRAINING_MEDIANS:

        raise HTTPException(
            status_code=500,
            detail=(
                "Training medians are not available "
                "in the churn model."
            )
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
            detail=(
                f"Could not read CSV: {str(e)}"
            )
        )


    # -----------------------------------------------------
    # Check empty CSV
    # -----------------------------------------------------

    if df.empty:

        raise HTTPException(
            status_code=400,
            detail=(
                "Uploaded CSV contains no rows."
            )
        )


    # =====================================================
    # SCHEMA ANALYSIS
    # =====================================================

    schema_result = analyze_schema(
        df,
        TRAINING_MEDIANS
    )


    # -----------------------------------------------------
    # Schema invalid
    # -----------------------------------------------------

    if not schema_result["valid"]:

        raise HTTPException(
            status_code=400,
            detail={

                "message":
                    schema_result["error"],

                "missing_columns":
                    schema_result[
                        "missing_columns"
                    ],

                "missing_count":
                    schema_result[
                        "missing_count"
                    ],

                "invalid_columns":
                    schema_result[
                        "invalid_columns"
                    ],

                "invalid_range_columns":
                    schema_result[
                        "invalid_range_columns"
                    ]
            }
        )


    # -----------------------------------------------------
    # Get cleaned DataFrame
    # -----------------------------------------------------

    df = schema_result[
        "dataframe"
    ]


    # =====================================================
    # MODEL INPUT
    # =====================================================

    X = df[
        FEATURE_COLUMNS
    ].copy()


    # =====================================================
    # CHURN PREDICTION
    # =====================================================

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
            detail=(
                f"Churn prediction failed: {str(e)}"
            )
        )


    # =====================================================
    # CUSTOMER RESULTS
    # =====================================================

    results = []


    for i in range(len(df)):

        customer = (
            df.iloc[i].to_dict()
        )


        # -------------------------------------------------
        # Churn result
        # -------------------------------------------------

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
                    "message":
                        "Behavior analysis failed.",

                    "error":
                        str(e)
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
                    "message":
                        "Recommendation engine failed.",

                    "error":
                        str(e)
                }
            )


        # -------------------------------------------------
        # Customer ID
        # -------------------------------------------------

        if "Phone Number" in df.columns:

            customer_id = (
                df.iloc[i][
                    "Phone Number"
                ]
            )

        elif "customerID" in df.columns:

            customer_id = (
                df.iloc[i][
                    "customerID"
                ]
            )

        elif "customer_id" in df.columns:

            customer_id = (
                df.iloc[i][
                    "customer_id"
                ]
            )

        else:

            customer_id = i


        # -------------------------------------------------
        # Final customer result
        # -------------------------------------------------

        results.append({

            "customer_id":
                str(customer_id),

            "churn_prediction":
                churn_prediction,

            "churn_probability":
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

    total = len(
        results
    )


    high_churn_count = sum(

        result[
            "churn_probability"
        ] >= 0.70

        for result in results
    )


    upsell_count = sum(

        result[
            "recommendation"
        ][
            "recommendation_type"
        ] == "UPSELL"

        for result in results
    )


    retention_count = sum(

        result[
            "recommendation"
        ][
            "recommendation_type"
        ] == "RETENTION"

        for result in results
    )


    no_recommendation_count = sum(

        result[
            "recommendation"
        ][
            "recommendation_type"
        ] == "NONE"

        for result in results
    )


    # =====================================================
    # RESPONSE
    # =====================================================

    return {

        "success":
            True,

        "filename":
            file.filename,

        "total":
            total,

        "schema_warnings":
            schema_result[
                "warnings"
            ],

        "missing_columns_filled":
            schema_result[
                "filled_columns"
            ],

        "renamed_columns":
            schema_result[
                "renamed_columns"
            ],

        "results":
            results,

        "summary": {

            "total":
                total,

            "high_churn_count":
                high_churn_count,

            "high_churn_percentage":
                round(
                    high_churn_count
                    / total
                    * 100,
                    2
                ),

            "upsell_count":
                upsell_count,

            "retention_count":
                retention_count,

            "no_recommendation_count":
                no_recommendation_count
        }
        
    }

@router.post("/generate-message")
def generate_outreach_message(
    data: MessageRequest,
    _: dict = Depends(get_current_admin)
):

    try:

        message = generate_message(
            customer_id=data.customer_id,
            recommendation_type=data.recommendation_type,
            plan_name=data.plan_name,
            plan_benefit=data.plan_benefit,
            reason=data.reason,
            churn_probability=data.churn_probability
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Message generation failed: {str(e)}"
        )

    return {
        "customer_id": data.customer_id,
        "message": message
    }