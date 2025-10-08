from typing import Optional
from datetime import date, datetime
from enum import Enum
from pydantic import BaseModel


class TaskStatus(Enum):
    PENDING = 'pending'
    IN_PROGRESS = 'in-progress'
    COMPLETED = 'completed'

class TaskPriority(Enum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'

class TaskUpdate(BaseModel):
    task_name: Optional[str] = None
    user_id: Optional[int] = None
    status: Optional[TaskStatus] = None
    due_date: Optional[date] = None
    priority: Optional[TaskPriority] = None

class TaskCreate(BaseModel):
    task_name: str
    user_id: int
    status: TaskStatus
    due_date: date
    priority: TaskPriority

class UserCreate(BaseModel):
    username: str
    role: str
    created_at: datetime

class UserUpdate(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None
    created_at: Optional[datetime] = None
