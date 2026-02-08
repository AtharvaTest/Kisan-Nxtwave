from app.db.mongo import db

class DecisionRepo:
    def create(self, doc: dict):
        db.decisions.insert_one(doc)
        return doc

    def get_by_evidence(self, evidence_id: str):
        return db.decisions.find_one({"evidence_id": evidence_id}, sort=[("made_at", -1)])

decision_repo = DecisionRepo()
