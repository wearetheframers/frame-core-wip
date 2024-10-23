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
from frame.src.services import ExecutionContext
from frame.src.framer.agency.priority import Priority


class ExploreEnvironmentAction(BaseAction):
    def __init__(self):
        super().__init__(
            "explore_environment", "Explore the environment", Priority.MEDIUM
        )

    async def execute(self, execution_context: ExecutionContext) -> str:
        prompt = "Describe an interesting environment that an AI agent might explore."
        response = await execution_context.llm_service.get_completion(prompt)
        return f"Explored environment: {response}"


async def main():
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

    # Register the ExploreEnvironmentAction
    explore_action = ExploreEnvironmentAction()
    framer.brain.action_registry.add_action(explore_action)

    # Set roles and goals from the config
    framer.roles = config.roles or []
    framer.goals = config.goals or []

    # Update the agency, brain, and execution context with the new roles and goals
    framer.agency.set_roles(framer.roles)
    framer.agency.set_goals(framer.goals)
    framer.execution_context.set_roles(framer.roles)
    framer.execution_context.set_goals(framer.goals)
    framer.execution_context.set_roles(framer.roles)
    framer.execution_context.set_goals(framer.goals)

    # Execute the explore environment action
    result = await framer.brain.execute_action("explore_environment", {})
    print(f"Task result: {result}")

    await framer.close()


if __name__ == "__main__":
    asyncio.run(main())
