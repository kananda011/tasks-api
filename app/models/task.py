from datetime import date, datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel,Field, field_validator

class Status(str, Enum):
    pending = 'pending'
    in_progress = 'in_progress'
    completed = 'completed'
    cancelled = 'cancelled'

class Priority(str, Enum):
    low = 'low'
    medium = 'medium'
    high = 'high'   

class TaskCreate(BaseModel):
    title: str = Field(None,min_length=3, max_length=100)
    description: Optional[str] = None
    status: Optional [Status] = None
    priority: Optional [Priority] = None
    due_date: Optional[date] = None

    @field_validator('due_date')
    def due_date_not_in_past(cls, v: Optional[date]):
        if v is not None and v < date.today():
            raise ValueError('Due date não pode ser no passado')
        return v

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None,min_length=3, max_length=100)
    description: Optional[str] = None
    status: Optional [Status] = None
    priority: Optional [Priority] = None
    due_date: Optional[date] = None

    @field_validator('due_date')
    @classmethod
    def due_date_not_in_past(cls, v: Optional[date]):
        if v is not None and v < date.today():
            raise ValueError('Due date não pode ser no passado')
        return v

class TaskOut(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    status: Status
    priority: Priority
    due_date: date
    created_at: datetime
    updated_at: datetime