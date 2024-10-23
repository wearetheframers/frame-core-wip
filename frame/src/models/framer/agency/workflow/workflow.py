from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from frame.src.framer.agency.tasks.task import Task
from frame.src.framer.agency.tasks.status import TaskStatus

class Workflow(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    tasks: List[Task] = Field(default_factory=list)
    status: str = "pending"
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    is_async: bool = False
    final_task: Optional[Task] = None

    def add_task(self, task: Task):
        self.tasks.append(task)
        self.updated_at = datetime.now()
