from typing import Optional, List
from fastapi import APIRouter, status
from app.models.task import TaskCreate, TaskUpdate, TaskOut, Status, Priority
from app.services.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])
service= TaskService()

@router.post("", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate):
    return service.create(payload.model_dump())

@router.get("", response_model=List[TaskOut])
def list_tasks(status: Optional[Status] = None, priority: Optional[Priority] = None):
    return service.List(status.value if status else None, priority.value if priority else None)

@router.get("/{task_id_}", response_model=TaskOut)
def get_task(task_id_: str):
    return service.get(task_id_)

@router.put("/{task_id_}", response_model=TaskOut)
def update_task(task_id_: str, payload: TaskUpdate):
    changes = {k: v for k, v in payload.model_dump().items() if v is not None}
    return service.update(task_id_, changes)

@router.delete("/{task_id_}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id_: str):
    service.delete(task_id_)
    return None
