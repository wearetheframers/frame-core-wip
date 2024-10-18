import sys
import os
import asyncio
from frame import Frame, FramerConfig
from frame.src.framer.agency.actions import BaseAction
from frame.src.services.execution_context import ExecutionContext
from frame.src.framer.agency.priority import Priority

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

class StreamingResponseAction(BaseAction):
    def __init__(self):
        super().__init__("streaming_response", "Generate a streaming response", Priority.MEDIUM)

    async def execute(self, execution_context: ExecutionContext, prompt: str) -> str:
        result = await execution_context.llm_service.get_completion(prompt, stream=True)
        streamed_response = ""
        print("Streamed Response:")
        async for chunk in result:
            print(chunk, end="", flush=True)
            streamed_response += chunk
        print("\n")
        return streamed_response

async def main():
    frame = Frame()
    config = FramerConfig(name="Example Framer", default_model="gpt-3.5-turbo")
    framer = await frame.create_framer(config)

    # Register the StreamingResponseAction
    streaming_action = StreamingResponseAction()
    framer.brain.action_registry.register_action(streaming_action)

    prompt = "Write a short story about an AI learning to understand human emotions."

    # Execute the streaming response action
    result = await framer.brain.action_registry.execute_action("streaming_response", {"prompt": prompt})

    print("Final Streamed Response Result:", result)

    await framer.close()

if __name__ == "__main__":
    asyncio.run(main())
