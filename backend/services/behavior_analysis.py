# Thresholds calculated from the 75th percentile
# of the original company dataset.

THRESHOLDS = {
    "intl_mins": 22.8,
    "intl_calls": 8,
    "intl_charge": 4.94,

    "night_mins": 329.2,
    "night_calls": 224,
    "night_charge": 20.44,

    "vmail_message": 22
}


def analyze_behavior(row):

    # -------- International usage --------
    intl_score = 0

    if row["Intl Mins"] >= THRESHOLDS["intl_mins"]:
        intl_score += 1

    if row["Intl Calls"] >= THRESHOLDS["intl_calls"]:
        intl_score += 1

    if row["Intl Charge"] >= THRESHOLDS["intl_charge"]:
        intl_score += 1

    if intl_score >= 2:
        international = "HIGH"
    elif intl_score == 1:
        international = "MEDIUM"
    else:
        international = "LOW"


    # -------- Night usage --------
    night_score = 0

    if row["Night Mins"] >= THRESHOLDS["night_mins"]:
        night_score += 1

    if row["Night Calls"] >= THRESHOLDS["night_calls"]:
        night_score += 1

    if row["Night Charge"] >= THRESHOLDS["night_charge"]:
        night_score += 1

    if night_score >= 2:
        night = "HIGH"
    elif night_score == 1:
        night = "MEDIUM"
    else:
        night = "LOW"


    # -------- Voice Mail usage --------
    if row["VMail Message"] >= THRESHOLDS["vmail_message"]:
        voicemail = "HIGH"
    elif row["VMail Message"] > 0:
        voicemail = "MEDIUM"
    else:
        voicemail = "LOW"


    return {
        "international_usage": international,
        "night_usage": night,
        "voicemail_usage": voicemail
    }