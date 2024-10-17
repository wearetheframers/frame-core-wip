from frame.src.models.framer.agency.roles import Roles, Role, RoleStatus as RolesModel, RoleModel, RoleStatusModel

from typing import List

class Roles(RoleModel):
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
