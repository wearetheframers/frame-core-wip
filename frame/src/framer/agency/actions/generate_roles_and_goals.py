def generate_roles_and_goals(self) -> None:
    """
    Generate roles and goals for the Framer.

    Args:
        framer (Framer): The current Framer instance.
    """
    roles, goals = self.agency.generate_roles_and_goals()
    self.agency.set_roles(roles)
    self.agency.set_goals(goals)
