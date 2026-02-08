from pymongo import MongoClient
from app.config import settings

client = None
db = None


def init_mongo() -> None:
    global client, db
    client = MongoClient(settings.mongo_uri)
    db = client[settings.mongo_db]
