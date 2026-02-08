from fastapi import APIRouter, Depends

from app.deps import ROLE_ADMIN, ROLE_FORENSIC, ROLE_JUDGE, ROLE_POLICE, assert_case_access, require_roles
from app.repositories.audit_repo import audit_repo
from app.repositories.evidence_repo import evidence_repo

router = APIRouter(tags=["audit"])


@router.get("/cases/{case_id}/timeline")
def case_timeline(case_id: str, user=Depends(require_roles(ROLE_POLICE, ROLE_FORENSIC, ROLE_JUDGE, ROLE_ADMIN))):
    assert_case_access(case_id, user)
    return audit_repo.by_case(case_id)


@router.get("/evidence/{evidence_id}/audit")
def evidence_audit(evidence_id: str, user=Depends(require_roles(ROLE_POLICE, ROLE_FORENSIC, ROLE_JUDGE, ROLE_ADMIN))):
    ev = evidence_repo.get(evidence_id)
    if ev:
        assert_case_access(ev["case_id"], user)
    return audit_repo.by_evidence(evidence_id)
