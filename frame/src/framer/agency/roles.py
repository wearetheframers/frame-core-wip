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
    def from_dict(cls, data: Dict[str, Any]) -> 'Role':
        return cls(**data)

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)

