from enum import Enum
from pydantic import BaseModel
from typing import Optional

class GoalStatus(Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    ABANDONED = "abandoned"

class Goal(BaseModel):
    name: str
    description: Optional[str] = None
    priority: int
    status: GoalStatus = GoalStatus.ACTIVE


