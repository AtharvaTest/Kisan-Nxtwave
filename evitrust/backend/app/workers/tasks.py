from app.workers.celery_app import celery_app
from app.repositories.evidence_repo import evidence_repo
from app.services.analysis_service import analysis_service
from app.services.audit_service import audit_service

@celery_app.task
def analyze_evidence(evidence_id: str):
    evidence = evidence_repo.get(evidence_id)
    if not evidence:
        return {"error": "not found"}
    audit_service.append_event(evidence["case_id"], evidence_id, "ANALYSIS_STARTED", {"actor": "SYSTEM"})
    doc = analysis_service.analyze_evidence(evidence)
    audit_service.append_event(evidence["case_id"], evidence_id, "ANALYSIS_DONE", {"actor": "SYSTEM", "risk_level": doc["risk_level"]})
    return {"ok": True, "analysis_id": doc["_id"]}
