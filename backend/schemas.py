from pydantic import BaseModel, EmailStr


class SignupRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class MessageRequest(BaseModel):
    customer_id: str
    recommendation_type: str
    plan_name: str | None = None
    plan_benefit: str | None = None
    reason: str
    churn_probability: float