import pandas as pd
import os


PLAN_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "plans",
    "plans.csv"
)

plans = pd.read_csv(PLAN_PATH)


def get_plan(trigger):
    plan = plans[plans["trigger"] == trigger]

    if plan.empty:
        return None

    return plan.iloc[0].to_dict()


def recommend(churn_probability, behavior):

    # 1. Retention gets highest priority
    if churn_probability >= 0.70:

        plan = get_plan("churn")

        return {
            "recommendation_type": "RETENTION",
            "plan": plan,
            "reason": "Customer has high churn probability"
        }


    # 2. International plan
    if behavior["international_usage"] == "HIGH":

        plan = get_plan("international")

        return {
            "recommendation_type": "UPSELL",
            "plan": plan,
            "reason": "High international calling usage"
        }


    # 3. Night plan
    if behavior["night_usage"] == "HIGH":

        plan = get_plan("night")

        return {
            "recommendation_type": "UPSELL",
            "plan": plan,
            "reason": "High night calling usage"
        }


    # 4. Voice-mail plan
    if behavior["voicemail_usage"] == "HIGH":

        plan = get_plan("voicemail")

        return {
            "recommendation_type": "UPSELL",
            "plan": plan,
            "reason": "High voice-mail usage"
        }


    # Nothing suitable
    return {
        "recommendation_type": "NONE",
        "plan": None,
        "reason": "No strong upsell opportunity detected"
    }