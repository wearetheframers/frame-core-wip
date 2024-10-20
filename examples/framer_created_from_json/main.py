import sys
import os
import asyncio

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from frame import Frame, FramerConfig
from frame.src.utils.config_parser import parse_json_config
from frame.src.framer.brain.actions import BaseAction
from frame.src.services.execution_context import ExecutionContext
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
    framer.brain.action_registry.register_action(explore_action)

    await framer.initialize()

    # Execute the explore environment action
    result = await framer.brain.action_registry.execute_action("explore_environment")
    print(f"Task result: {result}")

    await framer.close()


if __name__ == "__main__":
    asyncio.run(main())
