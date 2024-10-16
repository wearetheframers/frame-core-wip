from pydantic import BaseModel
from typing import List, Dict, Any

class Role(BaseModel):
    name: str
    description: str
    permissions: List[str] = []

class Roles(BaseModel):
    role_list: List[Role] = []

    def add_role(self, role: Role):
        self.role_list.append(role)

    def remove_role(self, role_name: str):
        self.role_list = [role for role in self.role_list if role.name != role_name]

    def evaluate_roles(self) -> List[Role]:
        # Implement evaluation logic here
        return self.role_list
