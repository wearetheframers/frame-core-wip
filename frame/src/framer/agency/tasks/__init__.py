from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional
import uuid


class TaskStatusModel(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class Task(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    description: str
    status: TaskStatusModel = Field(default=TaskStatusModel.PENDING)
    priority: float = Field(default=50.0, ge=0, le=100)
    workflow_id: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True
