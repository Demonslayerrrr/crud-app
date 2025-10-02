from typing import Optional
from datetime import date
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
    task_id: int
    task_name: str
    user_id: int
    status: TaskStatus
    due_date: date
    priority: TaskPriority
