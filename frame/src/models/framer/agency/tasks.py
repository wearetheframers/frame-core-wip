from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from .priority import Priority

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELED = "canceled"

class Task(BaseModel):
    id: str
    description: str
    priority: Priority = Field(default=Priority.MEDIUM)
    status: TaskStatus = TaskStatus.PENDING
    workflow_id: Optional[str] = None

class Tasks(BaseModel):
    tasks: list[Task] = []
