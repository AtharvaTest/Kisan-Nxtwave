from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException

from app.deps import ROLE_ADMIN, ROLE_FORENSIC, ROLE_JUDGE, ROLE_POLICE, assert_case_access, require_roles
from app.models.decision import DecisionCreate
from app.repositories.decision_repo import decision_repo
from app.repositories.evidence_repo import evidence_repo
from app.services.audit_service import audit_service
from app.utils.ids import new_id

router = APIRouter(tags=["decisions"])


@router.post("/evidence/{evidence_id}/decision")
def post_decision(evidence_id: str, payload: DecisionCreate, user=Depends(require_roles(ROLE_FORENSIC, ROLE_ADMIN))):
    ev = evidence_repo.get(evidence_id)
    if not ev:
        raise HTTPException(404, "Evidence not found")
    assert_case_access(ev["case_id"], user, write=True)
    doc = {
        "_id": new_id(),
        "evidence_id": evidence_id,
        "decision": payload.decision,
        "reviewer": {"name": user["name"], "role": user["role"], "email": user["email"]},
        "comment": payload.comment,
        "made_at": datetime.now(timezone.utc).isoformat(),
    }
    decision_repo.create(doc)
    evidence_repo.update_status(evidence_id, "DECIDED")
    audit_service.append_event(
        ev["case_id"],
        evidence_id,
        "DECISION",
        {
            "decision": payload.decision,
            "comment": payload.comment,
            "actor_user_id": user["_id"],
            "actor_role": user["role"],
            "actor_name": user["name"],
            "actor_email": user["email"],
        },
    )
    return doc


@router.get("/evidence/{evidence_id}/decision")
def get_decision(evidence_id: str, user=Depends(require_roles(ROLE_POLICE, ROLE_FORENSIC, ROLE_JUDGE, ROLE_ADMIN))):
    ev = evidence_repo.get(evidence_id)
    if not ev:
        raise HTTPException(404, "Evidence not found")
    assert_case_access(ev["case_id"], user)
    d = decision_repo.get_by_evidence(evidence_id)
    if not d:
        raise HTTPException(404, "No decision")
    return d
