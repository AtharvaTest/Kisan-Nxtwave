from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException

from app.db.mongo import db
from app.deps import ROLE_ADMIN, ROLE_FORENSIC, ROLE_JUDGE, ROLE_POLICE, assert_case_access, require_roles
from app.models.admin import UserCreate
from app.models.admin_extra import CaseAssignCreate
from app.repositories.user_repo import user_repo
from app.utils.ids import new_id

router = APIRouter(tags=["admin"])


@router.get("/admin/search")
def admin_search(
    risk: str | None = None,
    type: str | None = None,
    status: str | None = None,
    user=Depends(require_roles(ROLE_ADMIN)),
):
    pipeline = [{"$lookup": {"from": "analysis_results", "localField": "_id", "foreignField": "evidence_id", "as": "analysis"}}]
    q = {}
    if type:
        q["type"] = type
    if status:
        q["status"] = status
    if q:
        pipeline.insert(0, {"$match": q})
    if risk:
        pipeline.append({"$match": {"analysis.0.risk_level": risk}})
    return list(db.evidence.aggregate(pipeline))


@router.post("/admin/users")
def create_user(payload: UserCreate, user=Depends(require_roles(ROLE_ADMIN))):
    doc = payload.model_dump()
    doc["_id"] = new_id()
    doc["is_active"] = True
    doc["created_at"] = datetime.now(timezone.utc).isoformat()
    return user_repo.create(doc)


@router.get("/admin/users")
def list_users(user=Depends(require_roles(ROLE_ADMIN))):
    return user_repo.list()


@router.patch("/admin/users/{user_id}/disable")
def disable(user_id: str, user=Depends(require_roles(ROLE_ADMIN))):
    db.users.update_one({"_id": user_id}, {"$set": {"is_active": False}})
    return {"ok": True}


@router.post("/admin/cases/{case_id}/assign")
def assign_case(case_id: str, payload: CaseAssignCreate, user=Depends(require_roles(ROLE_ADMIN))):
    target = db.users.find_one({"_id": payload.assigned_to_user_id})
    if not target:
        raise HTTPException(404, "Target user not found")
    role_map = {
        "POLICE_OFFICER": {"INVESTIGATOR"},
        "FORENSIC_ANALYST": {"FORENSIC_REVIEWER"},
        "JUDGE_LAWYER": {"COURT_VIEWER"},
        "ADMIN": {"INVESTIGATOR", "FORENSIC_REVIEWER", "COURT_VIEWER"},
    }
    if payload.role_in_case not in role_map.get(target["role"], set()):
        raise HTTPException(400, "role_in_case not compatible with user role")
    doc = {
        "_id": new_id(),
        "case_id": case_id,
        "assigned_to_user_id": payload.assigned_to_user_id,
        "assigned_by_user_id": user["_id"],
        "role_in_case": payload.role_in_case,
        "assigned_at": datetime.now(timezone.utc).isoformat(),
    }
    db.case_assignments.update_one(
        {"case_id": case_id, "assigned_to_user_id": payload.assigned_to_user_id},
        {"$set": doc},
        upsert=True,
    )
    return doc


@router.get("/cases/{case_id}/merkle")
def get_merkle(case_id: str, user=Depends(require_roles(ROLE_POLICE, ROLE_FORENSIC, ROLE_JUDGE, ROLE_ADMIN))):
    assert_case_access(case_id, user)
    m = db.case_merkle.find_one({"_id": case_id}) or {"_id": case_id, "merkle_root": None, "leaf_hashes": []}
    if user["role"] == ROLE_JUDGE:
        return {"_id": m["_id"], "merkle_root": m.get("merkle_root"), "updated_at": m.get("updated_at")}
    return m
