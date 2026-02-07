from typing import Optional,List,Dict, Any
from fastapi import HTTPException, status
from app.repositories.task_repo import TaskRepository

class TaskService:
    def __init__(self):
        self.repo=TaskRepository()

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self.repo.create(data)
    
    
    def List(self, status_: Optional[str], priority_: Optional[str]) -> List[Dict[str, Any]]:
        return self.repo.list(status=status_, priority=priority_)
    
    def get(self, id_: str) -> Dict[str, Any]:
        doc = self.repo.get_by_id(id_)
        if not doc:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task não encontrada")
        return doc

    def update(self, id_: str, changes: Dict[str, Any]) -> Dict[str, Any]:
        current = self.repo.get_by_id(id_)
        if not current:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task não encontrada")
        
        if current["status"] == "completed":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                detail="Task com status completed não pode ser atualizada")
        
        updated= self.repo.update(id_, changes)
        if not updated:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task não encontrada")
        return updated
    
    def delete(self, id_: str) -> None:
        ok = self.repo.delete(id_)
        if not ok:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task não encontrada")
        
