from typing import Tuple, List, Dict, Any


def generate_roles_and_goals(self) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Generate roles and goals for the Framer.

    Args:
        self: The current Framer instance.

    Returns:
        Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]: A tuple containing the generated roles and goals.
    """
    roles, goals = self.agency.generate_roles_and_goals()
    self.agency.set_roles(roles)
    self.agency.set_goals(goals)
    return roles, goals
