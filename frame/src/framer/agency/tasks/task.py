from datetime import datetime
from typing import Any, Dict, Optional, List, Callable
from datetime import datetime
from typing import Any, Dict, Optional, List
from frame.src.utils.id_generator import generate_id
from frame.src.framer.agency.priority import Priority
from frame.src.framer.agency.tasks.status import TaskStatus
from pydantic import BaseModel, Field
import logging

logger = logging.getLogger(__name__)

class Task(BaseModel):
    """
    Represents a task within the Frame-Core system.

    A Task is an actionable item that Framers work on. It includes a description
    of the action to be performed, a priority level, a status, and can store
    results and metadata.
    """

    id: str = Field(default_factory=generate_id)
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
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    subtasks: List["Task"] = Field(default_factory=list)

    stakeholders: Optional[List[Dict[str, Any]]] = None

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True
        json_encoders = {datetime: lambda v: v.isoformat()}

    def __init__(self, **data):
        super().__init__(**data)
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        logger.debug(f"Created new task with ID: {self.id}")

    def update_status(self, new_status: TaskStatus) -> None:
        self.status = new_status
        self.updated_at = datetime.now()
        if new_status == TaskStatus.COMPLETED:
            self.completed_at = datetime.now()

    def set_result(self, result: Any) -> None:
        self.result = result
        self.updated_at = datetime.now()

    def add_subtask(self, subtask: "Task") -> None:
        self.subtasks.append(subtask)
        subtask.parent_task_id = self.id

    def to_dict(self) -> Dict[str, Any]:
        return self.dict()
