from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from app.config import settings
from app.db.mongo import db
from app.repositories.user_repo import user_repo

bearer = HTTPBearer(auto_error=False)


ROLE_POLICE = "POLICE_OFFICER"
ROLE_FORENSIC = "FORENSIC_ANALYST"
ROLE_JUDGE = "JUDGE_LAWYER"
ROLE_ADMIN = "ADMIN"


def create_token(user_id: str, role: str) -> str:
    payload = {
        "sub": user_id,
        "role": role,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_expire_minutes),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def get_current_user(credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer)):
    if not credentials:
        raise HTTPException(status_code=401, detail="Missing token")
    try:
        payload = jwt.decode(credentials.credentials, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    except JWTError as e:
        raise HTTPException(status_code=401, detail="Invalid token") from e
    user = user_repo.get(payload.get("sub"))
    if not user or not user.get("is_active", True):
        raise HTTPException(status_code=401, detail="Inactive or missing user")
    return user


def require_roles(*roles: str):
    def _inner(user=Depends(get_current_user)):
        if user.get("role") not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
        return user

    return _inner


def assert_case_access(case_id: str, user: dict, write: bool = False):
    if user["role"] == ROLE_ADMIN:
        return
    case = db.cases.find_one({"_id": case_id})
    if not case:
        raise HTTPException(404, "Case not found")

    if user["role"] == ROLE_POLICE:
        if write and case["created_by"]["email"] != user["email"]:
            raise HTTPException(403, "Police write access denied")
        assignment = db.case_assignments.find_one({"case_id": case_id, "assigned_to_user_id": user["_id"]})
        if case["created_by"]["email"] != user["email"] and not assignment:
            raise HTTPException(403, "Police read access denied")
        return

    assignment = db.case_assignments.find_one({"case_id": case_id, "assigned_to_user_id": user["_id"]})
    if not assignment:
        raise HTTPException(403, "Case assignment required")

    if user["role"] == ROLE_JUDGE and assignment.get("role_in_case") != "COURT_VIEWER":
        raise HTTPException(403, "Judge requires COURT_VIEWER assignment")
    if user["role"] == ROLE_FORENSIC and assignment.get("role_in_case") not in {"FORENSIC_REVIEWER", "INVESTIGATOR"}:
        raise HTTPException(403, "Forensic assignment role is invalid")

    if write and user["role"] == ROLE_JUDGE:
        raise HTTPException(403, "Judge is read-only")
