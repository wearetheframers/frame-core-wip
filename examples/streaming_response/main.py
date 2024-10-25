import sys
import os
import asyncio

# Add the project root to the Python path to ensure all modules can be imported correctly
# If we are running the examples from the source code (not installing package from pip)
# then you need to have this line uncommented.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from frame import Frame, FramerConfig
from frame.src.framer.brain.actions import BaseAction
from frame.src.services import ExecutionContext
from frame.src.framer.agency.priority import Priority


class StreamingResponseAction(BaseAction):
    def __init__(self):
        super().__init__(
            "streaming_response", "Generate a streaming response", Priority.MEDIUM
        )

    async def execute(self, execution_context: ExecutionContext, prompt: str) -> str:
        execution_context._streaming_response = {"status": "pending", "result": ""}
        await execution_context.llm_service.get_completion(prompt, stream=True)

        print("Streamed Response:")
        while execution_context._streaming_response["status"] == "pending":
            await asyncio.sleep(0.1)  # Check for new data every 100ms
            if execution_context._streaming_response["result"]:
                print(
                    execution_context._streaming_response["result"], end="", flush=True
                )
                execution_context._streaming_response["result"] = (
                    ""  # Clear after printing
                )

        if execution_context._streaming_response["status"] == "completed":
            print("\nStreaming completed.")
        elif execution_context._streaming_response["status"] == "error":
            print(
                f"\nAn error occurred: {execution_context._streaming_response['result']}"
            )

        return execution_context._streaming_response["result"]


async def main():
    frame = Frame()
    config = FramerConfig(name="Example Framer", default_model="gpt-3.5-turbo")
    framer = await frame.create_framer(config)

    # Register the StreamingResponseAction
    streaming_action = StreamingResponseAction()
    framer.brain.action_registry.add_action(streaming_action)

    prompt = "Write a short story about an AI learning to understand human emotions."

    # Execute the streaming response action
    result = await framer.brain.action_registry.execute_action(
        "streaming_response", prompt=prompt
    )

    print("Final Streamed Response Result:", result)

    await framer.close()


if __name__ == "__main__":
    asyncio.run(main())
