from frame.src.framer.brain.actions import BaseAction
from frame.src.framer.agency.priority import Priority
from frame.src.services import ExecutionContext

class StreamingResponseAction(BaseAction):
    def __init__(self):
        super().__init__(
            "streaming_response",
            "Generate a streaming response",
            Priority.MEDIUM
        )

    async def execute(self, execution_context: ExecutionContext, prompt: str) -> str:
        # Implementation of the action using the 'prompt' argument
        response = await execution_context.llm_service.get_completion(prompt)
        return f"Streaming response: {response}"
