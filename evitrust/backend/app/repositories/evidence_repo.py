from app.db.mongo import db

class EvidenceRepo:
    def create(self, doc: dict) -> dict:
        db.evidence.insert_one(doc)
        return doc

    def get(self, evidence_id: str):
        return db.evidence.find_one({"_id": evidence_id})

    def list_by_case(self, case_id: str):
        return list(db.evidence.find({"case_id": case_id}).sort("uploaded_at", -1))

    def find_duplicate_in_case(self, case_id: str, sha256: str):
        return db.evidence.find_one({"case_id": case_id, "sha256": sha256})

    def find_duplicate_global(self, sha256: str):
        return db.evidence.find_one({"sha256": sha256})

    def update_status(self, evidence_id: str, status: str):
        db.evidence.update_one({"_id": evidence_id}, {"$set": {"status": status}})

evidence_repo = EvidenceRepo()
