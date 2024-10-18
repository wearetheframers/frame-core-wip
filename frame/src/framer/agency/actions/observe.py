from typing import Optional
from frame.src.services.execution_context import ExecutionContext
from frame.src.framer.agency.actions.base_action import Action
from frame.src.models.framer.agency.priority import Priority

class ObserveAction(Action):
    def __init__(self):
        super().__init__("observe", "Process an observation and generate insights or actions", Priority.MEDIUM, str)

    async def execute(self, execution_context: ExecutionContext, observation: Optional[str] = None) -> str:
        """
        Process an observation and generate insights or actions.

        Args:
            execution_context (ExecutionContext): The execution context containing necessary services.
            observation (Optional[str]): The observation to process.

        Returns:
            str: Insights or actions based on the observation, or an error message if inputs are missing.
        """
        if observation is None:
            return "Observation skipped: missing observation"

        # Placeholder for observation processing logic
        print(f"Processing observation: {observation}")
        return f"Processed observation: {observation}"
