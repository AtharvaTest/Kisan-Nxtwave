from passlib.hash import bcrypt
from app.db.mongo import db

class UserRepo:
    def create(self, doc: dict):
        doc["password_hash"] = bcrypt.hash(doc.pop("password"))
        db.users.insert_one(doc)
        return doc

    def authenticate(self, email: str, password: str):
        user = db.users.find_one({"email": email})
        if not user:
            return None
        return user if bcrypt.verify(password, user["password_hash"]) else None

    def get(self, user_id: str):
        return db.users.find_one({"_id": user_id})

    def list(self):
        return list(db.users.find({}, {"password_hash": 0}))

user_repo = UserRepo()
