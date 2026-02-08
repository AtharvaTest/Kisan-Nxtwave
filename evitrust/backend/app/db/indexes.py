from app.db.mongo import db

def ensure_indexes() -> None:
    if db is None:
        return
    db.evidence.create_index([("case_id", 1), ("sha256", 1)], unique=True)
    db.evidence.create_index("sha256")
    db.audit_log.create_index([("case_id", 1), ("created_at", 1)])
    db.analysis_results.create_index([("evidence_id", 1), ("created_at", -1)])
    db.case_assignments.create_index([("case_id", 1), ("assigned_to_user_id", 1), ("role_in_case", 1)])
