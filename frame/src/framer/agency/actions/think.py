import asyncio
from typing import Dict, Any
from frame.src.framer.agency.execution_context import ExecutionContext


async def think(
    execution_context: ExecutionContext, thought: str = "Processing information..."
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
    # This function is now just a wrapper. The main logic is in the Brain's _execute_think_action method
    if execution_context.framer and execution_context.framer.brain:
        return await execution_context.framer.brain._execute_think_action(
            execution_context.framer.brain.make_decision(
                {"action": "think", "parameters": {"thought": thought}}
            )
        )
    else:
        return {"error": "Framer or Brain not available in execution context"}
