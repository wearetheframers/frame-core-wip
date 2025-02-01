from typing import List, Optional, Any
from pydantic import BaseModel, Field
from frame.src.framer.agency.priority import Priority
from enum import Enum


class TaskStatus(str, Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"


class Task(BaseModel):
    id: Optional[str] = None
    description: str
    status: TaskStatus = TaskStatus.PENDING
    priority: Priority = Field(default=Priority.MEDIUM)
    workflow_id: Optional[str] = None
    expected_results: List[Any] = Field(default_factory=list)
    subtasks: List["Task"] = Field(default_factory=list)
    updated_at: Optional[str] = None
    created_at: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True  # Allows self-referencing in 'subtasks'
        orm_mode = True  # Enables ORM mode if needed

    def to_dict(self):
        return self.dict()

    stakeholders: Optional[List[str]] = None  # Add this field
