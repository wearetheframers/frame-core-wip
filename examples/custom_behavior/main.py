import asyncio
from frame.frame import Frame
from frame.src.framer.config import FramerConfig


# Define a new custom action
async def custom_greet_action(execution_context, name: str) -> str:
    return f"Hello, {name}! Welcome to the custom behavior example."


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
    decision = await framer.brain.make_decision({"type": "greeting", "data": {"name": "Alice"}})
    if decision.action == "custom_greet":
        result = await framer.brain.execute_decision(decision)
        print(result)

    # Clean up
    await frame.close()

if __name__ == "__main__":
    asyncio.run(main())
