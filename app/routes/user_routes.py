from fastapi import APIRouter, HTTPException
from bson import ObjectId
from app.database import user_collection
from app.schemas import UserCreate, UserUpdate
from app.models import user_helper
from app.auth.auth_utils import verify_token
from fastapi import Depends
router = APIRouter()   # ✅ must be here


@router.post("/users")
def create_user(user: UserCreate):
    new_user = user_collection.insert_one(user.dict())
    created_user = user_collection.find_one({"_id": new_user.inserted_id})
    return user_helper(created_user)


@router.get("/users")
def get_users(user_id: str = Depends(verify_token)):
    users = []
    for user in user_collection.find():
        users.append(user_helper(user))
    return users


@router.get("/users/{user_id}")
def get_user(user_id: str):
    user = user_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        return user_helper(user)
    raise HTTPException(status_code=404, detail="User not found")


@router.put("/users/{user_id}")
def update_user(user_id: str, user: UserUpdate):
    update_data = {k: v for k, v in user.dict().items() if v is not None}

    if len(update_data) >= 1:
        result = user_collection.update_one(
            {"_id": ObjectId(user_id)}, {"$set": update_data}
        )

        if result.modified_count == 1:
            updated_user = user_collection.find_one({"_id": ObjectId(user_id)})
            return user_helper(updated_user)

    existing_user = user_collection.find_one({"_id": ObjectId(user_id)})
    if existing_user:
        return user_helper(existing_user)

    raise HTTPException(status_code=404, detail="User not found")


@router.delete("/users/{user_id}")
def delete_user(user_id: str):
    result = user_collection.delete_one({"_id": ObjectId(user_id)})

    if result.deleted_count == 1:
        return {"message": "User deleted"}

    raise HTTPException(status_code=404, detail="User not found")