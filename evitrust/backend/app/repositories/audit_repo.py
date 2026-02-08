from app.db.mongo import db

class AuditRepo:
    def append(self, doc: dict):
        db.audit_log.insert_one(doc)
        return doc

    def latest_by_case(self, case_id: str):
        return db.audit_log.find_one({"case_id": case_id}, sort=[("created_at", -1)])

    def by_case(self, case_id: str):
        return list(db.audit_log.find({"case_id": case_id}).sort("created_at", 1))

    def by_evidence(self, evidence_id: str):
        return list(db.audit_log.find({"evidence_id": evidence_id}).sort("created_at", 1))

audit_repo = AuditRepo()
