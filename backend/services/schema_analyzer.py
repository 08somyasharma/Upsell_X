import pandas as pd


# =========================================================
# REQUIRED MODEL FEATURES
# =========================================================

REQUIRED_COLUMNS = [
    "Account Length",
    "VMail Message",
    "Day Mins",
    "Day Calls",
    "Day Charge",
    "Eve Mins",
    "Eve Calls",
    "Eve Charge",
    "Night Mins",
    "Night Calls",
    "Night Charge",
    "Intl Mins",
    "Intl Calls",
    "Intl Charge",
    "CustServ Calls"
]


# =========================================================
# COLUMN ALIASES
# =========================================================

COLUMN_ALIASES = {

    "Account Length": [
        "Account Length",
        "account_length",
        "account length",
        "accountLength"
    ],

    "VMail Message": [
        "VMail Message",
        "vmail_message",
        "voicemail",
        "voice_mail_messages",
        "voicemail_messages"
    ],

    "Day Mins": [
        "Day Mins",
        "day_mins",
        "day minutes",
        "day_minutes",
        "dayMinutes"
    ],

    "Day Calls": [
        "Day Calls",
        "day_calls",
        "day calls",
        "dayCalls"
    ],

    "Day Charge": [
        "Day Charge",
        "day_charge",
        "day charge",
        "dayCharge"
    ],

    "Eve Mins": [
        "Eve Mins",
        "eve_mins",
        "evening_mins",
        "evening_minutes"
    ],

    "Eve Calls": [
        "Eve Calls",
        "eve_calls",
        "evening_calls"
    ],

    "Eve Charge": [
        "Eve Charge",
        "eve_charge",
        "evening_charge"
    ],

    "Night Mins": [
        "Night Mins",
        "night_mins",
        "night minutes",
        "night_minutes"
    ],

    "Night Calls": [
        "Night Calls",
        "night_calls",
        "night calls"
    ],

    "Night Charge": [
        "Night Charge",
        "night_charge",
        "night charge"
    ],

    "Intl Mins": [
        "Intl Mins",
        "intl_mins",
        "international_mins",
        "international_minutes",
        "international minutes"
    ],

    "Intl Calls": [
        "Intl Calls",
        "intl_calls",
        "international_calls",
        "international calls"
    ],

    "Intl Charge": [
        "Intl Charge",
        "intl_charge",
        "international_charge",
        "international charge"
    ],

    "CustServ Calls": [
        "CustServ Calls",
        "custserv_calls",
        "customer_service_calls",
        "customer service calls"
    ]
}


# =========================================================
# VALUE RANGES
# =========================================================
#
# These are broad sanity limits.
# The lower limit is 0 because these values cannot
# logically be negative.
#
# These are NOT the exact min/max values from the
# training dataset.
# =========================================================

VALUE_RANGES = {

    "Account Length": (0, 1000),

    "VMail Message": (0, 1000),

    "Day Mins": (0, 1000),
    "Day Calls": (0, 1000),
    "Day Charge": (0, 1000),

    "Eve Mins": (0, 1000),
    "Eve Calls": (0, 1000),
    "Eve Charge": (0, 1000),

    "Night Mins": (0, 1000),
    "Night Calls": (0, 1000),
    "Night Charge": (0, 1000),

    "Intl Mins": (0, 1000),
    "Intl Calls": (0, 1000),
    "Intl Charge": (0, 1000),

    "CustServ Calls": (0, 1000)
}


# =========================================================
# NORMALIZE COLUMN NAME
# =========================================================

def normalize_name(name):

    return (
        str(name)
        .strip()
        .lower()
        .replace("_", " ")
        .replace("-", " ")
    )


# =========================================================
# FIND MATCHING COLUMN
# =========================================================

def find_matching_column(
    dataframe_columns,
    expected_column
):

    aliases = COLUMN_ALIASES[
        expected_column
    ]

    normalized_uploaded = {
        normalize_name(column): column
        for column in dataframe_columns
    }

    for alias in aliases:

        normalized_alias = normalize_name(alias)

        if normalized_alias in normalized_uploaded:

            return normalized_uploaded[
                normalized_alias
            ]

    return None


# =========================================================
# SCHEMA ANALYZER
# =========================================================

def analyze_schema(
    df,
    training_medians
):

    df = df.copy()

    missing_columns = []
    filled_columns = []
    renamed_columns = []
    invalid_columns = []
    invalid_range_columns = []


    # =====================================================
    # 1. COLUMN NAME VALIDATION / NORMALIZATION
    # =====================================================

    rename_mapping = {}

    for expected_column in REQUIRED_COLUMNS:

        actual_column = find_matching_column(
            df.columns,
            expected_column
        )

        if actual_column is None:

            missing_columns.append(
                expected_column
            )

        elif actual_column != expected_column:

            rename_mapping[
                actual_column
            ] = expected_column

            renamed_columns.append({
                "from": actual_column,
                "to": expected_column
            })


    if rename_mapping:

        df = df.rename(
            columns=rename_mapping
        )


    # =====================================================
    # 2. REQUIRED COLUMN CHECK
    # =====================================================

    missing_count = len(
        missing_columns
    )


    # More than 3 missing → reject

    if missing_count > 3:

        return {
            "valid": False,
            "dataframe": None,
            "error":
                "Too many required columns are missing.",
            "missing_columns":
                missing_columns,
            "missing_count":
                missing_count,
            "filled_columns": [],
            "renamed_columns":
                renamed_columns,
            "invalid_columns": [],
            "invalid_range_columns": [],
            "warnings": []
        }


    # =====================================================
    # 3. FILL 1–3 MISSING COLUMNS
    #    USING TRAINING-DATA MEDIANS
    # =====================================================

    for column in missing_columns:

        if column not in training_medians:

            return {
                "valid": False,
                "dataframe": None,
                "error":
                    f"No training median available for "
                    f"'{column}'.",
                "missing_columns":
                    missing_columns,
                "missing_count":
                    missing_count,
                "filled_columns":
                    filled_columns,
                "renamed_columns":
                    renamed_columns,
                "invalid_columns": [],
                "invalid_range_columns": [],
                "warnings": []
            }


        df[column] = training_medians[
            column
        ]

        filled_columns.append({
            "column": column,
            "value":
                training_medians[column]
        })


    # =====================================================
    # 4. DATA TYPE VALIDATION
    # =====================================================

    for column in REQUIRED_COLUMNS:

        try:

            df[column] = pd.to_numeric(
                df[column],
                errors="raise"
            )

        except Exception:

            invalid_columns.append(
                column
            )


    # =====================================================
    # 5. INVALID DATA TYPE → REJECT
    # =====================================================

    if invalid_columns:

        return {
            "valid": False,
            "dataframe": None,
            "error":
                "Some required columns contain "
                "invalid or non-numeric values.",
            "missing_columns":
                missing_columns,
            "missing_count":
                missing_count,
            "filled_columns":
                filled_columns,
            "renamed_columns":
                renamed_columns,
            "invalid_columns":
                invalid_columns,
            "invalid_range_columns": [],
            "warnings": []
        }


    # =====================================================
    # 6. VALUE / RANGE VALIDATION
    # =====================================================

    for column in REQUIRED_COLUMNS:

        minimum, maximum = VALUE_RANGES[
            column
        ]

        invalid_values = (
            (df[column] < minimum)
            |
            (df[column] > maximum)
        )

        if invalid_values.any():

            invalid_range_columns.append({

                "column":
                    column,

                "minimum_allowed":
                    minimum,

                "maximum_allowed":
                    maximum,

                "invalid_row_count":
                    int(
                        invalid_values.sum()
                    )
            })


    # =====================================================
    # 7. INVALID RANGE → REJECT
    # =====================================================

    if invalid_range_columns:

        return {
            "valid": False,
            "dataframe": None,
            "error":
                "Some columns contain values "
                "outside the allowed range.",
            "missing_columns":
                missing_columns,
            "missing_count":
                missing_count,
            "filled_columns":
                filled_columns,
            "renamed_columns":
                renamed_columns,
            "invalid_columns": [],
            "invalid_range_columns":
                invalid_range_columns,
            "warnings": []
        }


    # =====================================================
    # 8. WARNINGS
    # =====================================================

    warnings = []


    if renamed_columns:

        warnings.append(
            "Some column names were normalized."
        )


    if filled_columns:

        warnings.append(
            "Missing columns were filled using "
            "training-data median values."
        )


    # =====================================================
    # 9. FINAL RESULT
    # =====================================================

    return {

        "valid": True,

        "dataframe":
            df,

        "error":
            None,

        "missing_columns":
            missing_columns,

        "missing_count":
            missing_count,

        "filled_columns":
            filled_columns,

        "renamed_columns":
            renamed_columns,

        "invalid_columns":
            [],

        "invalid_range_columns":
            [],

        "warnings":
            warnings
    }