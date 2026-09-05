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

# =========================================================
# COLUMN ALIASES
# =========================================================
# Allows common variations and meaningful synonyms for
# the model feature names.
#
# All aliases are converted back to the standard model
# feature names before prediction.
# =========================================================

COLUMN_ALIASES = {

    # -----------------------------------------------------
    # ACCOUNT LENGTH
    # -----------------------------------------------------

    "Account Length": [
        "Account Length",
        "account_length",
        "account length",
        "accountLength",
        "account duration",
        "account age",
        "customer account length",
        "customer account duration",
        "tenure",
        "customer tenure",
        "subscription length",
        "subscription duration"
    ],


    # -----------------------------------------------------
    # VOICEMAIL
    # -----------------------------------------------------

    "VMail Message": [
        "VMail Message",
        "vmail_message",
        "vmail messages",
        "voicemail",
        "voice mail",
        "voice_mail",
        "voice_mail_messages",
        "voicemail_messages",
        "voicemail messages",
        "number of voicemail messages",
        "voicemail count",
        "voice mail count",
        "vm count",
        "vm messages"
    ],


    # -----------------------------------------------------
    # DAY MINUTES
    # -----------------------------------------------------

    "Day Mins": [
        "Day Mins",
        "day_mins",
        "day mins",
        "day minutes",
        "day_minutes",
        "dayMinutes",
        "daily minutes",
        "daily_mins",
        "daytime minutes",
        "daytime_mins",
        "daytime calling minutes",
        "day calling minutes",
        "day call minutes",
        "daily calling minutes",
        "daily call minutes",
        "day talk time",
        "daily talk time",
        "daytime talk time"
    ],


    # -----------------------------------------------------
    # DAY CALLS
    # -----------------------------------------------------

    "Day Calls": [
        "Day Calls",
        "day_calls",
        "day calls",
        "dayCalls",
        "daily calls",
        "daily_calls",
        "daytime calls",
        "daytime_calls",
        "day calling count",
        "day call count",
        "daily call count",
        "number of day calls",
        "number of daytime calls",
        "day call volume"
    ],


    # -----------------------------------------------------
    # DAY CHARGE
    # -----------------------------------------------------

    "Day Charge": [
        "Day Charge",
        "day_charge",
        "day charge",
        "dayCharge",
        "daily charge",
        "daily_charge",
        "daytime charge",
        "daytime_charge",
        "day cost",
        "daily cost",
        "day calling cost",
        "day call cost",
        "day usage charge",
        "day usage cost"
    ],


    # -----------------------------------------------------
    # EVENING MINUTES
    # -----------------------------------------------------

    "Eve Mins": [
        "Eve Mins",
        "eve_mins",
        "eve mins",
        "evening mins",
        "evening_mins",
        "evening minutes",
        "evening_minutes",
        "evening calling minutes",
        "evening call minutes",
        "evening call duration",
        "evening talk time",
        "evening usage minutes",
        "nighttime evening minutes"
    ],


    # -----------------------------------------------------
    # EVENING CALLS
    # -----------------------------------------------------

    "Eve Calls": [
        "Eve Calls",
        "eve_calls",
        "eve calls",
        "evening calls",
        "evening_calls",
        "evening call count",
        "evening calling count",
        "number of evening calls",
        "number of evening calls made",
        "evening call volume"
    ],


    # -----------------------------------------------------
    # EVENING CHARGE
    # -----------------------------------------------------

    "Eve Charge": [
        "Eve Charge",
        "eve_charge",
        "eve charge",
        "evening charge",
        "evening_charge",
        "evening cost",
        "evening calling cost",
        "evening call cost",
        "evening usage charge",
        "evening usage cost"
    ],


    # -----------------------------------------------------
    # NIGHT MINUTES
    # -----------------------------------------------------

    "Night Mins": [
        "Night Mins",
        "night_mins",
        "night mins",
        "night minutes",
        "night_minutes",
        "nighttime minutes",
        "nighttime_mins",
        "night calling minutes",
        "night call minutes",
        "night talk time",
        "nighttime talk time",
        "night usage minutes",
        "overnight minutes"
    ],


    # -----------------------------------------------------
    # NIGHT CALLS
    # -----------------------------------------------------

    "Night Calls": [
        "Night Calls",
        "night_calls",
        "night calls",
        "nightCalls",
        "nighttime calls",
        "nighttime_calls",
        "night call count",
        "nighttime call count",
        "number of night calls",
        "number of nighttime calls",
        "night call volume"
    ],


    # -----------------------------------------------------
    # NIGHT CHARGE
    # -----------------------------------------------------

    "Night Charge": [
        "Night Charge",
        "night_charge",
        "night charge",
        "nightCharge",
        "nighttime charge",
        "nighttime_charge",
        "night cost",
        "nighttime cost",
        "night calling cost",
        "night call cost",
        "night usage charge",
        "night usage cost"
    ],


    # -----------------------------------------------------
    # INTERNATIONAL MINUTES
    # -----------------------------------------------------

    "Intl Mins": [
        "Intl Mins",
        "intl_mins",
        "intl mins",
        "international_mins",
        "international mins",
        "international_minutes",
        "international minutes",
        "international calling minutes",
        "international call minutes",
        "international call duration",
        "international talk time",
        "international usage minutes",
        "international usage",
        "overseas calling minutes",
        "international voice minutes"
    ],


    # -----------------------------------------------------
    # INTERNATIONAL CALLS
    # -----------------------------------------------------

    "Intl Calls": [
        "Intl Calls",
        "intl_calls",
        "intl calls",
        "international_calls",
        "international calls",
        "internationalCalls",
        "international call count",
        "international calling count",
        "number of international calls",
        "number of international calls made",
        "international call volume",
        "overseas calls",
        "overseas call count"
    ],


    # -----------------------------------------------------
    # INTERNATIONAL CHARGE
    # -----------------------------------------------------

    "Intl Charge": [
        "Intl Charge",
        "intl_charge",
        "intl charge",
        "international_charge",
        "international charge",
        "internationalCharge",
        "international cost",
        "international calling cost",
        "international call cost",
        "international usage charge",
        "international usage cost",
        "international fees",
        "overseas calling cost"
    ],


    # -----------------------------------------------------
    # CUSTOMER SERVICE CALLS
    # -----------------------------------------------------

    "CustServ Calls": [
        "CustServ Calls",
        "custserv_calls",
        "custserv calls",
        "customer_service_calls",
        "customer service calls",
        "customerServiceCalls",
        "customer service call count",
        "customer support calls",
        "customer support call count",
        "support calls",
        "support call count",
        "service calls",
        "service call count",
        "help desk calls",
        "helpdesk calls",
        "number of customer service calls",
        "number of support calls"
    ]
}

# =========================================================
# VALUE RANGES
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
                "Provided file contains neg values",
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