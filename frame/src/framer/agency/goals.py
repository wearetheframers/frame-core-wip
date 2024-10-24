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


from enum import Enum
from typing import List, Dict, Any


class GoalStatus(str, Enum):
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    ABANDONED = "ABANDONED"


class Goal:
    def __init__(
        self,
        name: str,
        description: str,
        priority: int = 5,
        status: GoalStatus = GoalStatus.ACTIVE,
    ):
        self.name = name
        self.description = description
        self.priority = priority
        self.status = status

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "priority": self.priority,
            "status": self.status.value,
        }


from enum import Enum
from typing import Dict, Any


class GoalStatus(Enum):
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    ABANDONED = "ABANDONED"


class Goal:
    def __init__(
        self,
        name: str,
        description: str,
        priority: int = 5,
        status: GoalStatus = GoalStatus.ACTIVE,
    ):
        self.name = name
        self.description = description
        self.priority = priority
        self.status = status

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "priority": self.priority,
            "status": self.status.value,
        }
