from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class WorkflowModel(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    tasks: List[str] = Field(default_factory=list)
    status: str = "pending"
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
