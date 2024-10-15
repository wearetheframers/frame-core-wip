from typing import Any
from frame.src.framer.agency.execution_context import ExecutionContext


async def research(execution_context: ExecutionContext, research_topic: str) -> str:
    """
    Perform research on a given topic and summarize findings.

    Args:
        execution_context (ExecutionContext): The execution context containing necessary services.
        research_topic (str): The research topic.

    Returns:
        str: A summary of the research findings.
    """
    print(f"Performing research on topic: {research_topic}")

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

    return f"Research findings for topic '{research_topic}':\n{result}"
