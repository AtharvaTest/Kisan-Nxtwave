from fastapi import APIRouter, Depends, HTTPException

from app.deps import ROLE_ADMIN, ROLE_FORENSIC, ROLE_JUDGE, ROLE_POLICE, assert_case_access, require_roles
from app.repositories.analysis_repo import analysis_repo
from app.repositories.audit_repo import audit_repo
from app.repositories.evidence_repo import evidence_repo
from app.services.audit_service import audit_service
from app.services.report_service import report_service
from app.services.storage_service import storage_service

router = APIRouter(tags=["reports"])


@router.get("/evidence/{evidence_id}/report.pdf")
def report(evidence_id: str, user=Depends(require_roles(ROLE_POLICE, ROLE_FORENSIC, ROLE_JUDGE, ROLE_ADMIN))):
    ev = evidence_repo.get(evidence_id)
    an = analysis_repo.latest(evidence_id)
    if not ev or not an:
        raise HTTPException(404, "Missing evidence/analysis")
    assert_case_access(ev["case_id"], user)

    events = audit_repo.by_evidence(evidence_id)
    latest = events[-1]["entry_hash"] if events else ""
    code = f"EVT-{ev['sha256'][:12].upper()}-{latest[-6:].upper()}"

    from app.db.mongo import db

    merkle = db.case_merkle.find_one({"_id": ev["case_id"]}) or {}
    pdf = report_service.build_pdf(ev, an, latest, code, merkle.get("merkle_root", "N/A"))
    key = f"{ev['case_id']}/{evidence_id}/reports/report.pdf"
    report_service.store_pdf(key, pdf)
    audit_service.append_event(
        ev["case_id"],
        evidence_id,
        "REPORT_EXPORTED",
        {
            "key": key,
            "actor_user_id": user["_id"],
            "actor_role": user["role"],
            "actor_name": user["name"],
            "actor_email": user["email"],
        },
    )
    return {"url": storage_service.presigned_get(key), "verification_code": code}
