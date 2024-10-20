from typing import Dict, Any
from frame.src.services.execution_context import ExecutionContext
from frame.src.framer.brain.actions import BaseAction
from frame.src.framer.agency.priority import Priority


class RespondAction(BaseAction):
    def __init__(self):
        super().__init__(
            "respond",
            "Generate a default response based on the current context if NO memory retrieval is needed. If any type of personal information or questions about some previously saved or stored or recorded information is referenced, then likely this respond action is not appropriate and we need to use the memory response.",
            2,
        )

    async def execute(
        self, execution_context: ExecutionContext, **kwargs
    ) -> Dict[str, Any]:
        """
        Generate a response based on the current context, emphasizing the most recent perception.

        Args:
            execution_context (ExecutionContext): The execution context containing necessary services.
            **kwargs: Additional keyword arguments that might be passed to the action.

        Returns:
            Dict[str, Any]: A dictionary containing the generated response.
        """
        llm_service = execution_context.llm_service
        soul = execution_context.soul

        # Get the most recent perception
        recent_perception = execution_context.get_state(
            "recent_perception", "No recent perception available."
        )

        # Get recent memories and perceptions
        recent_memories = (
            execution_context.memory_service.get_recent_memories(5)
            if execution_context.memory_service
            else []
        )
        recent_perceptions = execution_context.get_state("recent_perceptions", [])[-5:]

        # Get roles, goals, and soul information
        roles = execution_context.get_state("roles", [])
        goals = execution_context.get_state("goals", [])
        soul_state = soul.get_current_state() if soul else {}

        # Get the content from kwargs if provided, otherwise use recent_perception
        content = kwargs.get("content", recent_perception)

        # Construct the prompt
        prompt = f"""
        As an AI assistant with the following characteristics:
        
        Roles: {roles}
        Goals: {goals}
        Soul: {soul_state}
        
        Recent memories: {recent_memories}
        Recent perceptions: {recent_perceptions}
        
        You are responding to the following input:
        {content}
        
        Please generate a response that takes into account all of the above information, 
        with particular emphasis on addressing the given input.
        
        Response:
        """

        # Get the completion from the language model
        response = await llm_service.get_completion(prompt)

        return {"response": response.strip()}
