from typing import Dict, Any
from frame.src.services.execution_context import ExecutionContext
from frame.src.framer.agency.actions.base import BaseAction
from frame.src.framer.agency.priority import Priority


class ResearchAction(BaseAction):
    def __init__(self):
        super().__init__(
            "research",
            "Perform research on a given topic and summarize findings",
            Priority.HIGH,
        )

    async def execute(
        self, execution_context: ExecutionContext, research_topic: str
    ) -> Dict[str, Any]:
        """
        Perform research on a given topic and summarize findings.

        Args:
            execution_context (ExecutionContext): The execution context containing necessary services.
            research_topic (str): The research topic.

        Returns:
            Dict[str, Any]: A dictionary containing the research findings and any additional information.
        """
        print(f"Performing research on topic: {research_topic}")

        if execution_context.llm_service is None:
            return {
                "error": f"Unable to perform research on '{research_topic}' due to missing LLM service."
            }

        # Use the LLM service from the execution context
        result = await execution_context.llm_service.get_completion(
            f"Provide a summary of the latest developments and top libraries for {research_topic}",
            model=execution_context.llm_service.default_model,
        )

        # If memory service is available, store the research results
        if execution_context.memory_service:
            await execution_context.memory_service.add_memory(
                f"Research on {research_topic}", result
            )

        return {
            "topic": research_topic,
            "findings": result,
            "summary": f"Research findings for topic '{research_topic}':\n{result}",
        }
