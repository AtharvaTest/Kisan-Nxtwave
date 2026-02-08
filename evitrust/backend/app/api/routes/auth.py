from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException

from app.deps import ROLE_ADMIN, create_token, get_current_user, require_roles
from app.models.admin import UserCreate
from app.models.auth import LoginRequest
from app.repositories.user_repo import user_repo
from app.utils.ids import new_id

router = APIRouter(tags=["auth"])


@router.post("/auth/register")
def register(payload: UserCreate, user=Depends(require_roles(ROLE_ADMIN))):
    doc = payload.model_dump()
    doc["_id"] = new_id()
    doc["is_active"] = True
    doc["created_at"] = datetime.now(timezone.utc).isoformat()
    return user_repo.create(doc)


@router.post("/auth/login")
def login(payload: LoginRequest):
    user = user_repo.authenticate(payload.email, payload.password)
    if not user:
        raise HTTPException(401, "Invalid credentials")
    token = create_token(user["_id"], user["role"])
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "_id": user["_id"],
            "name": user["name"],
            "email": user["email"],
            "role": user["role"],
            "department": user.get("department"),
        },
    }


@router.get("/auth/me")
def me(user=Depends(get_current_user)):
    user.pop("password_hash", None)
    return user
