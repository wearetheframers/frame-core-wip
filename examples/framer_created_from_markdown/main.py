import sys
import os
import asyncio

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from frame import Frame, FramerConfig
from frame.src.utils.config_parser import parse_markdown_config
from frame.src.framer.agency.actions import BaseAction
from frame.src.services.execution_context import ExecutionContext
from frame.src.framer.agency.priority import Priority


class EngageConversationAction(BaseAction):
    def __init__(self):
        super().__init__(
            "engage_conversation", "Engage in a deep conversation", Priority.HIGH
        )

    async def execute(self, execution_context: ExecutionContext) -> str:
        prompt = "Let's have a deep conversation about the nature of consciousness and artificial intelligence."
        response = await execution_context.llm_service.get_completion(prompt)
        return f"Engaged in a deep conversation: {response}"


async def main():
    possible_paths = [
        os.path.join(os.path.dirname(__file__), "framer.md"),
        os.path.join(
            os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), "framer.md"
        ),
        os.path.join(
            os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")),
            "framer.md",
        ),
    ]

    config = None
    for path in possible_paths:
        try:
            config = parse_markdown_config(path)
            break
        except FileNotFoundError:
            continue

    if config is None:
        raise FileNotFoundError("config.md not found in any of the expected locations.")

    frame = Frame()
    config_dict = config.__dict__ if isinstance(config, FramerConfig) else config
    framer = await frame.create_framer(FramerConfig(**config_dict))

    # Register the EngageConversationAction
    engage_action = EngageConversationAction()
    framer.brain.action_registry.register_action(engage_action)

    await framer.initialize()

    # Execute the engage conversation action
    result = await framer.brain.action_registry.execute_action("engage_conversation")
    print(f"Task result: {result}")

    await framer.close()


if __name__ == "__main__":
    asyncio.run(main())
