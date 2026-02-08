from fastapi import APIRouter, Depends, HTTPException

from app.deps import ROLE_ADMIN, ROLE_FORENSIC, ROLE_JUDGE, ROLE_POLICE, assert_case_access, require_roles
from app.repositories.analysis_repo import analysis_repo
from app.repositories.evidence_repo import evidence_repo
from app.workers.tasks import analyze_evidence

router = APIRouter(tags=["analysis"])


@router.post("/evidence/{evidence_id}/analyze")
def trigger_analysis(evidence_id: str, user=Depends(require_roles(ROLE_POLICE, ROLE_FORENSIC, ROLE_ADMIN))):
    ev = evidence_repo.get(evidence_id)
    if not ev:
        raise HTTPException(404, "Evidence not found")
    assert_case_access(ev["case_id"], user, write=True)
    evidence_repo.update_status(evidence_id, "ANALYZING")
    job = analyze_evidence.delay(evidence_id)
    return {"job_id": job.id}


@router.get("/evidence/{evidence_id}/analysis")
def latest_analysis(evidence_id: str, user=Depends(require_roles(ROLE_POLICE, ROLE_FORENSIC, ROLE_JUDGE, ROLE_ADMIN))):
    ev = evidence_repo.get(evidence_id)
    if not ev:
        raise HTTPException(404, "Evidence not found")
    assert_case_access(ev["case_id"], user)
    r = analysis_repo.latest(evidence_id)
    if not r:
        raise HTTPException(404, "No analysis")
    return r
