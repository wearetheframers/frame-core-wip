from typing import Dict, Any
from frame.src.services.execution_context import ExecutionContext
from frame.src.framer.agency.actions import BaseAction
from frame.src.framer.agency.priority import Priority


class ThinkAction(BaseAction):
    def __init__(self):
        super().__init__(
            "think",
            "Ponder and reflect on the current situation and current state of self.",
            1,
        )

    async def execute(
        self,
        execution_context: ExecutionContext,
        thought: str = "Processing information...",
    ) -> Dict[str, Any]:
        """
        Ponder and reflect on the current situation, potentially creating new tasks or generating a new prompt.
        This action is only necessary if a new prompt should be generated with new pretext and context for better results.

        Args:
            execution_context (ExecutionContext): The execution context containing necessary services.
            thought (str): The initial thought or idea to process.

        Returns:
            Dict[str, Any]: A dictionary containing the results of the thinking process.
        """
        if execution_context and execution_context.brain:
            return await execution_context.brain._execute_think_action(
                execution_context.brain.make_decision(
                    {"action": "think", "parameters": {"thought": thought}}
                )
            )
        else:
            return {"error": "Brain not available in execution context"}
