from datetime import datetime, timezone
from app.db.mongo import db

class CaseRepo:
    def create(self, doc: dict) -> dict:
        doc["created_at"] = datetime.now(timezone.utc).isoformat()
        db.cases.insert_one(doc)
        return doc

    def list_for_user(self, user: dict):
        if user["role"] == "ADMIN":
            return list(db.cases.find().sort("created_at", -1))
        created = list(db.cases.find({"created_by.email": user["email"]}))
        assigned = list(db.case_assignments.find({"assigned_to_user_id": user["_id"]}))
        ids = {c["_id"] for c in created} | {a["case_id"] for a in assigned}
        return list(db.cases.find({"_id": {"$in": list(ids)}}))

    def get(self, case_id: str):
        return db.cases.find_one({"_id": case_id})

case_repo = CaseRepo()
