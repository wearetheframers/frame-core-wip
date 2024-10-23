import sys
import os

# Add the project root to the Python path to ensure all modules can be imported correctly
# If we are running the examples from the source code (not installing package from pip)
# then you need to have this line uncommented.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from frame.src.framer.brain.actions import BaseAction
from frame.src.framer.agency.priority import Priority
from frame.src.services.context.execution_context_service import ExecutionContext
from typing import Optional
import asyncio
from frame import Frame, FramerConfig


class CustomGreetAction(BaseAction):
    def __init__(self):
        super().__init__(
            name="custom_greet",
            description="Greet a user with a custom message",
            priority=Priority.HIGH,  # High priority to ensure preference over default actions
        )

    async def execute(self, execution_context: ExecutionContext, **kwargs) -> str:
        custom_message = kwargs.get("custom_message", "Hello")
        name = kwargs.get("name", "User")
        return f"{custom_message} Nice to meet you, {name}!"


async def main():
    # Initialize Frame and create a Framer
    frame = Frame()
    config = FramerConfig(name="CustomBehaviorFramer", default_model="gpt-3.5-turbo")
    framer = await frame.create_framer(config)

    # Create an instance of your custom action
    custom_action = CustomGreetAction()

    # Register the custom action
    framer.brain.action_registry.add_action(custom_action)

    # Set up the execution context
    execution_context = ExecutionContext(llm_service=framer.llm_service)
    framer.execution_context = execution_context
    framer.brain.action_registry.set_execution_context(execution_context)
    # Create a perception dictionary that includes the necessary data
    perception = {
        "type": "user_input",
        "data": {"name": "Alice", "custom_message": "Hello"},
    }

    # Process the perception to get a decision
    decision = await framer.brain.process_perception(perception)
    if decision.action == "custom_greet":
        result = await framer.brain.execute_decision(decision)
        print(result["response"])  # Adjust based on the structure of the result

    # Clean up
    # Perform any necessary cleanup here
    # For example, if there are resources to release, do it here
    print("Cleaning up resources...")


if __name__ == "__main__":
    asyncio.run(main())


if __name__ == "__main__":
    asyncio.run(main())
