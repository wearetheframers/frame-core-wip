from typing import List
from frame.src.models.framer.agency.roles import RoleStatus, Role
from frame.src.models.framer.agency.priority import Priority


class Roles:
    """
    Manages a collection of roles for a Framer.

    This class provides methods to add, remove, update, and manage roles.
    It allows for dynamic role management within the Framer's agency.

    Attributes:
        roles (List[Role]): A list of Role objects representing the current roles.
    """

    def __init__(self):
        self.roles: List[Role] = []

    def add_role(self, role: Role):
        """
        Add a new role to the collection.

        Args:
            role (Role): The role to be added.
        """
        if isinstance(role.priority, str):
            role.priority = Priority.from_string(role.priority)
        elif not isinstance(role.priority, Priority):
            role.priority = Priority.MEDIUM
        self.roles.append(role)

    def remove_role(self, role_id: str):
        """
        Remove a role from the collection based on its ID.

        Args:
            role_id (str): The ID of the role to be removed.
        """
        self.roles = [role for role in self.roles if role.id != role_id]

    def get_roles(self) -> List[Role]:
        """
        Retrieve all roles in the collection.

        Returns:
            List[Role]: A list of all current roles.
        """
        return self.roles

    def clear_roles(self):
        """
        Remove all roles from the collection.
        """
        self.roles = []

    def update_role(self, role_id: str, updated_role: Role):
        """
        Update an existing role with new information.

        Args:
            role_id (str): The ID of the role to be updated.
            updated_role (Role): The new role information to replace the existing role.
        """
        for i, role in enumerate(self.roles):
            if role.id == role_id:
                self.roles[i] = updated_role
                break

    def update_role_status(self, role_id: str, status: RoleStatus):
        """
        Update the status of a specific role.

        Args:
            role_id (str): The ID of the role to update.
            status (RoleStatus): The new status to set for the role.
        """
        for role in self.roles:
            if role.id == role_id:
                role.status = status
                break
