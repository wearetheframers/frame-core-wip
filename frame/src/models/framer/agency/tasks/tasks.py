from pydantic import BaseModel, Field
from typing import Optional, List, Any, Dict
from enum import Enum
from frame.src.framer.agency.priority import Priority
from frame.src.framer.agency.tasks.status import TaskStatus


class TaskModel(BaseModel):
    id: str
    description: str
    priority: Priority = Field(default=Priority.MEDIUM)
    workflow_id: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDING
    expected_results: List[Any] = Field(default_factory=list)
    dependencies: List[str] = Field(default_factory=list)
    parent_task_id: Optional[str] = None
    assigned_to: Optional[str] = None
    estimated_duration: Optional[float] = None
    tags: List[str] = Field(default_factory=list)
    type: Optional[str] = None
    data: Dict[str, Any] = Field(default_factory=dict)
    result: Optional[Any] = None
    subtasks: List["TaskModel"] = Field(default_factory=list)
    updated_at: Optional[str] = None
    created_at: Optional[str] = None
