from pydantic import BaseModel, Field
from typing import Optional, List, Any
from enum import Enum
from frame.src.framer.agency.priority import Priority
from frame.src.models.framer.agency.tasks import TaskStatus


class TaskModel(BaseModel):
    id: str
    description: str
    priority: Priority = Field(default=Priority.MEDIUM)
    status: TaskStatus = TaskStatus.PENDING
    workflow_id: Optional[str] = None
    expected_results: List[Any] = Field(default_factory=list)
    subtasks: List["TaskModel"] = Field(default_factory=list)
    updated_at: Optional[str] = None
    created_at: Optional[str] = None


class TasksModel(BaseModel):
    tasks: list[TaskModel] = []
