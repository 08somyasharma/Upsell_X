from fastapi import APIRouter, HTTPException, Response

from database import admins_collection
from schemas import SignupRequest, LoginRequest

from auth.utils import (
    hash_password,
    verify_password,
    create_access_token
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# =========================
# SIGNUP
# =========================

@router.post("/signup")
def signup(data: SignupRequest):

    existing_admin = admins_collection.find_one({
        "email": data.email
    })

    if existing_admin:
        raise HTTPException(
            status_code=400,
            detail="Admin already exists"
        )

    admin = {
        "name": data.name,
        "email": data.email,
        "password_hash": hash_password(data.password)
    }

    admins_collection.insert_one(admin)

    return {
        "message": "Admin created successfully"
    }


# =========================
# LOGIN
# =========================

@router.post("/login")
def login(
    data: LoginRequest,
    response: Response
):

    admin = admins_collection.find_one({
        "email": data.email
    })

    if not admin:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Compare entered password with stored hash
    if not verify_password(
        data.password,
        admin["password_hash"]
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Create JWT
    token = create_access_token(
        admin["email"]
    )

    # Store JWT in browser cookie
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=3600
    )

    return {
        "message": "Login successful"
    }