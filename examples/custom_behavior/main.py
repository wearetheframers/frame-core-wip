import sys
import os

# Import Frame from upper dir
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from typing import Optional
import asyncio
from frame import Frame, FramerConfig


# Define a new custom action
async def custom_greet_action(
    execution_context, custom_message: str, name: Optional[str] = "User"
) -> str:
    return f"{custom_message} Nice to meet you, {name}!"


async def main():
    # Initialize Frame and create a Framer
    frame = Frame()
    config = FramerConfig(name="CustomBehaviorFramer", default_model="gpt-3.5-turbo")
    framer = await frame.create_framer(config)

    # Register the custom action
    # Setting a high priority ensures that this action is preferred over others,
    # such as the default `respond` action, in the decision-making process.
    framer.brain.action_registry.register_action(
        "custom_greet",
        custom_greet_action,
        description="Greet a user with a custom message",
        priority=10,  # High priority to ensure preference over default actions
    )

    # Example usage of the custom action
    decision = await framer.brain.make_decision(
        {"type": "custom_greet", "data": {"name": "Alice", "custom_message": "Hello"}}
    )
    if decision.action == "custom_greet":
        result = await framer.brain.execute_decision(decision)
        print(result)

    # Clean up
    # Perform any necessary cleanup here
    # For example, if there are resources to release, do it here
    print("Cleaning up resources...")


if __name__ == "__main__":
    asyncio.run(main())
