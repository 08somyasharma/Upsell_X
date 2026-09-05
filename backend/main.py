from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from auth.routes import router as auth_router
from routes.prediction import router as prediction_router


app = FastAPI(
    title="Upsell & Churn Prediction API",
    version="1.0.0"
)

# Allowed origins for development
origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "http://127.0.0.1:8080",
    "http://localhost:8080",
    "http://127.0.0.1:3000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)
app.include_router(prediction_router)


@app.get("/health")
def health():
    return {
        "status": "ok"
    }