from typing import Dict, Any
from frame.src.framer.config import FramerConfig
from frame.src.framer.brain.actions import BaseAction
from frame.src.services import ExecutionContext


class CreateNewAgentAction(BaseAction):
    def __init__(self):
        super().__init__(
            "create_new_agent", "Create a new agent with the required properties", 2
        )

    async def execute(
        self, execution_context: ExecutionContext, config: Dict[str, Any]
    ) -> Any:
        """
        Create a new agent with the required properties.

        Args:
            execution_context (ExecutionContext): The execution context containing necessary services.
            config (Dict[str, Any]): Configuration for the new agent.

        Returns:
            Framer: The newly created Framer instance.
        """
        new_config = FramerConfig(**config)
        new_framer = await execution_context.create_framer(new_config)
        return new_framer
