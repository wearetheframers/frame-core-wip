from typing import Tuple, List, Dict, Any
from frame.src.services.execution_context import ExecutionContext
from frame.src.framer.agency.actions.base_action import Action

class GenerateRolesAndGoalsAction(Action):
    def __init__(self):
        super().__init__("generate_roles_and_goals", "Generate roles and goals for the Framer")

    async def execute(self, execution_context: ExecutionContext) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Generate roles and goals for the Framer.

        Args:
            execution_context (ExecutionContext): The execution context containing necessary services.

        Returns:
            Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]: A tuple containing the generated roles and goals.
        """
        agency = execution_context.agency
        roles, goals = await agency.generate_roles_and_goals()
        agency.set_roles(roles)
        agency.set_goals(goals)
        return roles, goals
