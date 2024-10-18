from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, Any
from .priority import Priority

class GoalStatus(Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    ABANDONED = "abandoned"

class Goal(BaseModel):
    name: str
    description: Optional[str] = None
    priority: Priority = Field(default=Priority.MEDIUM)
    status: GoalStatus = GoalStatus.ACTIVE

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)

