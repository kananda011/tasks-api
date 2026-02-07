from pymongo import MongoClient
from app.core.config import MONGO_URI, MONGO_DB, MONGO_COLLECTION
_client = None

def get_collection():
    global _client
    if _client is None: 
        _client = MongoClient(MONGO_URI)
    db = _client[MONGO_DB]
    return db[MONGO_COLLECTION]
