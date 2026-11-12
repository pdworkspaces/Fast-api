from fastapi import APIRouter, HTTPException
from app.database import user_collection
from app.auth.auth_utils import hash_password, verify_password, create_access_token
from app.auth.auth_schemas import SignupModel, LoginModel
from app.models import user_helper

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup")
def signup(user: SignupModel):
    existing_user = user_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pwd = hash_password(user.password)

    new_user = {
        "name": user.name,
        "email": user.email,
        "password": hashed_pwd
    }

    result = user_collection.insert_one(new_user)
    created_user = user_collection.find_one({"_id": result.inserted_id})

    token = create_access_token({"user_id": str(created_user["_id"])})

    return {
        "access_token": token,
        "user": user_helper(created_user)
    }

@router.post("/login")
def login(user: LoginModel):
    db_user = user_collection.find_one({"email": user.email})

    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"user_id": str(db_user["_id"])})

    return {
        "access_token": token,
        "user": user_helper(db_user)
    }