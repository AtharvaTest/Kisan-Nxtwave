from app.db.mongo import db

class AnalysisRepo:
    def create(self, doc: dict):
        db.analysis_results.insert_one(doc)
        return doc

    def latest(self, evidence_id: str):
        return db.analysis_results.find_one({"evidence_id": evidence_id}, sort=[("created_at", -1)])

analysis_repo = AnalysisRepo()
