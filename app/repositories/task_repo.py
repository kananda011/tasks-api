from datetime import datetime, date, time
from pydoc import doc
from typing import Optional, List, Dict, Any
from bson import ObjectId
from app.utils.mongo import get_collection

def _normalize_due_date(payload: Dict[str, Any]) -> Dict[str, Any]:
    
    if "due_date" in payload and isinstance(payload["due_date"], date) and not isinstance(payload["due_date"], datetime):
        payload["due_date"] = datetime.combine(payload["due_date"], time.min)
    return payload

def _serialize(doc: Dict[str, Any]) -> Dict[str, Any]:
    doc["id"] = str(doc.pop("_id"))
 
    if "due_date" in doc and isinstance(doc["due_date"], datetime):
        doc["due_date"] = doc["due_date"].date()
 
    return doc

class TaskRepository:
    def __init__(self):
        self.col=get_collection()

    def create(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        now = datetime.utcnow()
 
        payload = _normalize_due_date(payload)
 
        payload.update({
            "status": payload.get("status", "pending"),
            "created_at": now,
            "updated_at": now,
    })
        res = self.col.insert_one(payload)
        doc = self.col.find_one({"_id": res.inserted_id})
        return _serialize(doc)
    
    def list(self,status: Optional[str]=None, priority: Optional[str]=None) -> List[Dict[str, Any]]:
        query={}
        if status:
            query['status']=status
        if priority:
            query['priority']=priority
        docs=self.col.find(query).sort("created_at",-1)
        return [_serialize(d) for d in docs]

    def get_by_id(self, id_: str) -> Optional[Dict[str, Any]]:
        if not ObjectId.is_valid(id_):
            return None
        doc=self.col.find_one({"_id": ObjectId(id_)})
        return _serialize(doc) if doc else None
    
    def update(self, id_: str, changes: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not ObjectId.is_valid(id_):
            return None
 
        changes = _normalize_due_date(changes)
 
        changes["updated_at"] = datetime.utcnow()
        res = self.col.update_one({"_id": ObjectId(id_)}, {"$set": changes})
        if res.matched_count == 0:
            return None
        doc = self.col.find_one({"_id": ObjectId(id_)})
        return _serialize(doc)
    
    def delete(self, id_: str) -> bool:
        if not ObjectId.is_valid(id_):
            return False
        res=self.col.delete_one({"_id": ObjectId(id_)})
        return res.deleted_count == 1