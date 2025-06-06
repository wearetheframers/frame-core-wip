from typing import Optional, Dict, Any
from frame.src.framer.brain.actions import BaseAction
from frame.src.services import ExecutionContext
from frame.src.framer.agency.priority import Priority
from frame.src.utils.decorators import log_execution, measure_performance


class ObserveAction(BaseAction):
    def __init__(self):
        super().__init__(
            "observe",
            "Process an observation and generate insights or actions",
            1,
        )

    @log_execution
    @measure_performance
    async def execute(
        self,
        execution_context: ExecutionContext,
        observation: Optional[str] = None,
        insights: Optional[Dict[str, Any]] = None,
        actions: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None,
        next_steps: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Process an observation and generate insights or actions.

        Args:
            execution_context (ExecutionContext): The execution context containing necessary services.
            observation (Optional[str]): The observation to process.
            insights (Optional[Dict[str, Any]]): Additional insights to consider during observation.

        Returns:
            str: Insights or actions based on the observation, or an error message if inputs are missing.
        """
        if observation is None and insights is None:
            return "Observation skipped: missing observation and insights"

        # Placeholder for observation processing logic
        print(f"Processing observation: {observation}")
        if insights:
            print(f"Additional insights: {insights}")

        insights_str = ", ".join(f"{k}: {v}" for k, v in (insights or {}).items())
        return (
            f"Processed observation: {observation}\nAdditional insights: {insights_str}"
        )
