def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "name": user.get("name"),
        "email": user.get("email"),
        "age": user.get("age"),   # ✅ safe (returns None if missing)
    }