from fastapi import APIRouter, HTTPException
from models.db import conn
from schemas.user import User
import bcrypt


user = APIRouter()


@user.post("/signup")
def signup(user_data: User):

    # Check if email already exists
    existing_user = conn.local.users.find_one({
        "email": user_data.email
    })

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    # Hash password
    hashed_password = bcrypt.hashpw(
        user_data.password.encode("utf-8"),
        bcrypt.gensalt()
    )

    new_user = {
        "name": user_data.name,
        "email": user_data.email,
        "password": hashed_password.decode("utf-8")
    }

    result = conn.local.users.insert_one(new_user)

    return {
        "message": "Account created successfully",
        "id": str(result.inserted_id)
    }


@user.post("/login")
def login(user_data: User):

    existing_user = conn.local.users.find_one({
        "email": user_data.email
    })

    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    password_match = bcrypt.checkpw(
        user_data.password.encode("utf-8"),
        existing_user["password"].encode("utf-8")
    )

    if not password_match:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    return {
        "message": "Login successful",
        "id": str(existing_user["_id"]),
        "name": existing_user["name"],
        "email": existing_user["email"]
    }