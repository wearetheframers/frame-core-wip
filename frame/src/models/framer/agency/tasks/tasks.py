from pydantic import BaseModel, Field
from typing import Optional, List, Any
from enum import Enum
from frame.src.framer.agency.priority import Priority
from .task_status import TaskStatus


class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELED = "canceled"


class TaskModel(BaseModel):
    id: str
    description: str
    priority: Priority = Field(default=Priority.MEDIUM)
    status: TaskStatus = TaskStatus.PENDING
    workflow_id: Optional[str] = None
    expected_results: List[Any] = Field(default_factory=list)


class TasksModel(BaseModel):
    tasks: list[TaskModel] = []
