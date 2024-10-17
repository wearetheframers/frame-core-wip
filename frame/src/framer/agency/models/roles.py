from pydantic import BaseModel, Field
from typing import List, Dict, Any

class Role(BaseModel):
    id: str
    name: str
    description: str
    permissions: List[str] = []
    priority: int = Field(default=5, ge=1, le=10)

class Roles(BaseModel):
    role_list: List[Role] = []

    def add_role(self, role: Role):
        self.role_list.append(role)

    def remove_role(self, role_id: str):
        self.role_list = [role for role in self.role_list if role.id != role_id]

    def get_roles(self) -> List[Role]:
        return self.role_list

    def clear_roles(self):
        self.role_list = []

    def update_role(self, role_id: str, updated_role: Role):
        for i, role in enumerate(self.role_list):
            if role.id == role_id:
                self.role_list[i] = updated_role
                break
