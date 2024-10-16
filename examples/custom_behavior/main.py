import sys
import os

# Import Frame from upper dir
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
import asyncio
from frame import Frame, FramerConfig


# Define a new custom action
async def custom_greet_action(execution_context, custom_message: str) -> str:
    return custom_message


async def main():
    # Initialize Frame and create a Framer
    frame = Frame()
    config = FramerConfig(name="CustomBehaviorFramer", default_model="gpt-3.5-turbo")
    framer = await frame.create_framer(config)

    # Register the custom action
    framer.brain.action_registry.register_action(
        "custom_greet",
        custom_greet_action,
        description="Greet a user with a custom message",
        priority=5,
    )

    # Example usage of the custom action
    decision = await framer.brain.make_decision(
        {"type": "greeting", "data": {"name": "Alice"}}
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
