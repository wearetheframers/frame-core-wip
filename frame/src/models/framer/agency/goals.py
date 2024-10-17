from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional
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

class Goals(BaseModel):
    goals: list[Goal] = []
