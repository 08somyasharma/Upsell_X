import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage


load_dotenv()


# =========================================================
# LLM SETUP
# =========================================================

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.7,
    max_tokens=600
)


SYSTEM_PROMPT = (
    "You are a customer outreach assistant for a telecom company. "
    "Write a short, warm, professional message (2-3 sentences) to a "
    "customer, based on the recommendation given. Do not use emojis. "
    "Do not mention words like 'churn' or 'risk' directly to the "
    "customer — keep the tone customer-friendly and positive."
)


# =========================================================
# GENERATE MESSAGE
# =========================================================

def generate_message(
    customer_id,
    recommendation_type,
    plan_name,
    plan_benefit,
    reason,
    churn_probability
):

    # -----------------------------------------------------
    # RETENTION customers
    # -----------------------------------------------------

    if recommendation_type == "RETENTION":

        user_prompt = (
            f"Customer ID: {customer_id}\n"
            f"This customer has a high probability of leaving us "
            f"({round(churn_probability * 100)}%).\n"
            f"Internal reason flagged: {reason}\n\n"
            f"Write a short retention message that makes the customer "
            f"feel valued and offers them support, without sounding "
            f"desperate and without mentioning churn risk directly."
        )


    # -----------------------------------------------------
    # UPSELL customers
    # -----------------------------------------------------

    elif recommendation_type == "UPSELL":

        user_prompt = (
            f"Customer ID: {customer_id}\n"
            f"This customer is a good fit for: {plan_name}\n"
            f"Plan benefit: {plan_benefit}\n"
            f"Reason: {reason}\n\n"
            f"Write a short, friendly message recommending this plan "
            f"to the customer, highlighting the benefit clearly."
        )


    # -----------------------------------------------------
    # Nothing to send
    # -----------------------------------------------------

    else:

        return "No outreach message needed for this customer."


    # -----------------------------------------------------
    # CALL LLM
    # -----------------------------------------------------

    response = llm.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=user_prompt)
    ])

    return response.content.strip()