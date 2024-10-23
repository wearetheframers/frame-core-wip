import sys
import os
import asyncio

# Add the project root to the Python path to ensure all modules can be imported correctly
# If we are running the examples from the source code (not installing package from pip)
# then you need to have this line uncommented.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from frame import Frame, FramerConfig
from frame.src.utils.config_parser import parse_json_config
from frame.src.framer.brain.actions import BaseAction
import logging
from frame.src.services import ExecutionContext
from frame.src.framer.agency.priority import Priority


class ExploreEnvironmentAction(BaseAction):
    def __init__(self):
        super().__init__(
            "explore_environment", "Explore the environment", Priority.LOW
        )

    async def execute(self, execution_context: ExecutionContext) -> str:
        prompt = "Describe an interesting environment that an AI agent might explore."
        response = await execution_context.llm_service.get_completion(prompt)
        return f"Explored environment: {response}"


async def main():
    logger = logging.getLogger(__name__)
    possible_paths = [
        os.path.join(os.path.dirname(__file__), "framer.json"),
        os.path.join(
            os.path.abspath(os.path.join(os.path.dirname(__file__), "..")),
            "framer.json",
        ),
        os.path.join(
            os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")),
            "framer.json",
        ),
    ]

    config = None
    for path in possible_paths:
        try:
            config = parse_json_config(path)
            break
        except FileNotFoundError:
            continue

    if config is None:
        raise FileNotFoundError(
            "config.json not found in any of the expected locations."
        )

    frame = Frame()
    config_dict = config.__dict__ if isinstance(config, FramerConfig) else config
    framer = await frame.create_framer(FramerConfig(**config_dict))

    # Register actions from the config
    if hasattr(config, "actions"):
        for action_info in config.actions:
            action_name = action_info["name"]
            description = action_info["description"]
            priority_str = action_info["priority"]
            priority = getattr(Priority, priority_str, Priority.MEDIUM)

            # Dynamically create an action class
            def create_action_class(name, desc, prio):
                class DynamicAction(BaseAction):
                    def __init__(self):
                        super().__init__(name, desc, prio)

                    async def execute(self, execution_context: ExecutionContext) -> str:
                        prompt = desc
                        response = await execution_context.llm_service.get_completion(prompt)
                        return f"{name} executed: {response}"

                return DynamicAction()

            action_instance = create_action_class(action_name, description, priority)
            framer.brain.action_registry.add_action(action_instance)

    # Set roles and goals from the config
    framer.roles = config.roles or []
    framer.goals = config.goals or []

    # Update the agency, brain, and execution context with the new roles and goals
    framer.agency.set_roles(framer.roles)
    framer.agency.set_goals(framer.goals)
    framer.execution_context.set_roles(framer.roles)
    framer.execution_context.set_goals(framer.goals)

    # Execute the actions one by one
    # Ensure that the config has actions or handle it appropriately
    if hasattr(config, 'actions'):
        for action in config.actions:
            # Process actions if they exist
            pass
    if hasattr(config, 'actions') and config.actions:
        for action in config.actions:
            action_name = action["name"]
            prompt_text = action["description"]  # Use the description as the prompt
            if action_name == "streaming_response":
                result = await framer.brain.action_registry.execute_action(action_name, prompt=prompt_text)
            else:
                result = await framer.brain.action_registry.execute_action(action_name)
            print(f"Task result for '{action_name}': {result}")
    else:
        logger.warning("No actions found in the configuration.")

    await framer.close()


if __name__ == "__main__":
    asyncio.run(main())
