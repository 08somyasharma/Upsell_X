from fastapi import Request, HTTPException
import jwt

from auth.utils import SECRET_KEY, ALGORITHM
from database import admins_collection


def get_current_admin(request: Request):

    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        email = payload.get("sub")

        if not email:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

    except jwt.ExpiredSignatureError:

        raise HTTPException(
            status_code=401,
            detail="Token expired"
        )

    except jwt.InvalidTokenError:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    admin = admins_collection.find_one({
        "email": email
    })

    if not admin:

        raise HTTPException(
            status_code=401,
            detail="Admin not found"
        )

    return admin