import joblib
import pandas as pd

from services.behavior_analysis import analyze_behavior
from services.recommendation_engine import recommend


# Load churn model
model_data = joblib.load("ml_models/churn_model.pkl")
churn_model = model_data["pipeline"]


# Test customer
customer = {
    "Account Length": 128,
    "VMail Message": 25,
    "Day Mins": 265.1,
    "Day Calls": 110,
    "Day Charge": 45.07,
    "Eve Mins": 197.4,
    "Eve Calls": 99,
    "Eve Charge": 16.78,
    "Night Mins": 400,
    "Night Calls": 250,
    "Night Charge": 20.0,
    "Intl Mins": 25,
    "Intl Calls": 10,
    "Intl Charge": 7.0,
    "CustServ Calls": 1
}


# Convert to DataFrame
df = pd.DataFrame([customer])


# Churn prediction
churn_prediction = churn_model.predict(df)[0]
churn_probability = churn_model.predict_proba(df)[0][1]


# Behavior analysis
behavior = analyze_behavior(customer)


# Recommendation
recommendation = recommend(
    churn_probability,
    behavior
)


print("\n========== CUSTOMER ANALYSIS ==========")

print("Churn:", int(churn_prediction))
print("Churn Probability:", round(churn_probability, 2))

print("\nBehavior:")
print("International:", behavior["international_usage"])
print("Night:", behavior["night_usage"])
print("Voice Mail:", behavior["voicemail_usage"])

print("\nRecommendation:")
print("Type:", recommendation["recommendation_type"])
print("Reason:", recommendation["reason"])

if recommendation["plan"]:
    print("Plan:", recommendation["plan"]["plan_name"])
    print("Price:", recommendation["plan"]["price"])
    print("Benefit:", recommendation["plan"]["benefit"])