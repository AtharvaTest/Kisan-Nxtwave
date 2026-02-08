from fastapi import APIRouter, Depends, HTTPException

from app.deps import ROLE_ADMIN, ROLE_FORENSIC, ROLE_JUDGE, ROLE_POLICE, assert_case_access, require_roles
from app.models.case import CaseCreate
from app.repositories.case_repo import case_repo
from app.utils.ids import new_id

router = APIRouter(tags=["cases"])


@router.post("/cases")
def create_case(payload: CaseCreate, user=Depends(require_roles(ROLE_POLICE, ROLE_ADMIN))):
    doc = {
        "_id": new_id(),
        "title": payload.title,
        "description": payload.description,
        "created_by": {"name": user["name"], "email": user["email"]},
        "status": "OPEN",
    }
    return case_repo.create(doc)


@router.get("/cases")
def list_cases(user=Depends(require_roles(ROLE_POLICE, ROLE_FORENSIC, ROLE_JUDGE, ROLE_ADMIN))):
    return case_repo.list_for_user(user)


@router.get("/cases/{case_id}")
def get_case(case_id: str, user=Depends(require_roles(ROLE_POLICE, ROLE_FORENSIC, ROLE_JUDGE, ROLE_ADMIN))):
    c = case_repo.get(case_id)
    if not c:
        raise HTTPException(404, "Case not found")
    assert_case_access(case_id, user)
    return c
