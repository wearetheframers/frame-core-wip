from pydantic import BaseModel, Field
from typing import Any, Dict, Optional, List
from datetime import datetime
from enum import Enum
from frame.src.models.framer.agency.priority import Priority


class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELED = "canceled"


class TaskModel(BaseModel):
    id: str
    workflow_id: str
    description: str
    priority: Priority = Field(default=Priority.MEDIUM)
    status: TaskStatus = TaskStatus.PENDING
    result: Optional[Any] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    expected_results: Optional[List[Any]] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    dependencies: List[str] = Field(default_factory=list)
    subtasks: List["TaskModel"] = Field(default_factory=list)
    parent_task_id: Optional[str] = None
    assigned_to: Optional[str] = None
    estimated_duration: Optional[float] = None
    actual_duration: Optional[float] = None
    tags: List[str] = Field(default_factory=list)
