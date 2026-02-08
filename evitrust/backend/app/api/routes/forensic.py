from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException

from app.db.mongo import db
from app.deps import ROLE_ADMIN, ROLE_FORENSIC, ROLE_JUDGE, ROLE_POLICE, assert_case_access, require_roles
from app.models.forensic import ForensicNoteCreate
from app.repositories.evidence_repo import evidence_repo
from app.services.audit_service import audit_service
from app.utils.ids import new_id

router = APIRouter(tags=["forensic"])


@router.post("/evidence/{evidence_id}/forensic-note")
def add_forensic_note(evidence_id: str, payload: ForensicNoteCreate, user=Depends(require_roles(ROLE_FORENSIC, ROLE_ADMIN))):
    ev = evidence_repo.get(evidence_id)
    if not ev:
        raise HTTPException(404, "Evidence not found")
    assert_case_access(ev["case_id"], user, write=True)

    note = {
        "_id": new_id(),
        "evidence_id": evidence_id,
        "case_id": ev["case_id"],
        "created_by_user_id": user["_id"],
        "note_text": payload.note_text,
        "recommendation": payload.recommendation,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    db.forensic_notes.insert_one(note)
    audit_service.append_event(
        ev["case_id"],
        evidence_id,
        "FORENSIC_NOTE_ADDED",
        {
            "recommendation": payload.recommendation,
            "actor_user_id": user["_id"],
            "actor_role": user["role"],
            "actor_name": user["name"],
            "actor_email": user["email"],
        },
    )
    return note


@router.get("/evidence/{evidence_id}/forensic-notes")
def by_evidence(evidence_id: str, user=Depends(require_roles(ROLE_POLICE, ROLE_FORENSIC, ROLE_JUDGE, ROLE_ADMIN))):
    ev = evidence_repo.get(evidence_id)
    if not ev:
        raise HTTPException(404, "Evidence not found")
    assert_case_access(ev["case_id"], user)
    return list(db.forensic_notes.find({"evidence_id": evidence_id}).sort("created_at", -1))


@router.get("/cases/{case_id}/forensic-notes")
def by_case(case_id: str, user=Depends(require_roles(ROLE_POLICE, ROLE_FORENSIC, ROLE_JUDGE, ROLE_ADMIN))):
    assert_case_access(case_id, user)
    return list(db.forensic_notes.find({"case_id": case_id}).sort("created_at", -1))
