from pydantic import BaseModel, Field
from typing import List, Dict, Any
from enum import Enum
from frame.src.framer.agency.priority import Priority


class RoleStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ABANDONED = "abandoned"


class Role(BaseModel):
    id: str
    name: str
    description: str
    permissions: List[str] = []
    priority: Priority = Field(default=Priority.MEDIUM)
    status: RoleStatus = RoleStatus.ACTIVE

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "permissions": self.permissions,
            "priority": self.priority.value,
            "status": self.status.value,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Role":
        return cls(**data)

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


from enum import Enum
from typing import List, Dict, Any


class RoleStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    SUSPENDED = "SUSPENDED"


class Role:
    def __init__(
        self,
        id: str,
        name: str,
        description: str,
        priority: int = 5,
        status: RoleStatus = RoleStatus.ACTIVE,
        permissions: List[str] = None,
    ):
        self.id = id
        self.name = name
        self.description = description
        self.priority = priority
        self.status = status
        self.permissions = permissions or []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "priority": self.priority,
            "status": self.status.value,
            "permissions": self.permissions,
        }
