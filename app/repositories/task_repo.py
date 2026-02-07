from datetime import datetime
from typing import Optional, List, Dict, Any
from bson import ObjectId
from app.utils.mongo import get_collection

def _sirealize(doc: Dict[str, Any]) -> Dict[str, Any]:
    doc['id'] = str(doc.pop("_id"))
    return doc

class TaskRepository:
    def __init__(self):
        self.col=get_collection()

    def create (self, payload: Dict[str, Any]) -> Dict[str, Any]:
        now = datetime.utcnow()
        payload.update({
            "status": payload.get("status", "pending"),
            "created_at": now,
        })
        res=self.col.insert_one(payload)
        doc=self.col.find_one({"_id": res.inserted_id})
        return _sirealize(doc)
    
    def list(self,status: Optional[str]=None, priority: Optional[str]=None) -> List[Dict[str, Any]]:
        query={}
        if status:
            query['status']=status
        if priority:
            query['priority']=priority
        docs=self.col.find(query).sort("created_at",-1)
        return [_sirealize(d) for d in docs]

    def get_by_id(self, id_: str) -> Optional[Dict[str, Any]]:
        if not ObjectId.is_valid(id_):
            return None
        doc=self.col.find_one({"_id": ObjectId(id_)})
        return _sirealize(doc) if doc else None
    
    def update(self, id_: str, changes: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not ObjectId.is_valid(id_):
            return None
        changes["updated_at"]= datetime.utcnow()
        res=self.col.update_one({"_id": ObjectId(id_)},{"$set": changes})
        if res.matched_count==0:
            return None
        doc=self.col.find_one({"_id": ObjectId(id_)})
        return _sirealize(doc)
    
    def delete(self, id_: str) -> bool:
        if not ObjectId.is_valid(id_):
            return False
        res=self.col.delete_one({"_id": ObjectId(id_)})
        return res.deleted_count == 1