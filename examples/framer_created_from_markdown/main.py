import sys
import os
import asyncio

# Add the project root to the Python path to ensure all modules can be imported correctly
# If we are running the examples from the source code (not installing package from pip)
# then you need to have this line uncommented.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from frame import Frame, FramerConfig
from frame.src.utils.config_parser import parse_markdown_config
from frame.src.framer.brain.actions import BaseAction
from frame.src.services import ExecutionContext
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
    framer.brain.action_registry.add_action(engage_action)

    await framer.initialize()

    # Execute the engage conversation action
    result = await framer.brain.action_registry.execute_action("engage_conversation")
    print(f"Task result: {result}")

    await framer.close()


if __name__ == "__main__":
    asyncio.run(main())
import sys
import os
import asyncio

# Add the project root to the Python path to ensure all modules can be imported correctly
# If we are running the examples from the source code (not installing package from pip)
# then you need to have this line uncommented.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from frame import Frame, FramerConfig
from frame.src.utils.config_parser import parse_markdown_config
from frame.src.framer.brain.actions import BaseAction
from frame.src.services import ExecutionContext
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


class TellStoryAction(BaseAction):
    def __init__(self):
        super().__init__(
            "tell_story", "Craft and narrate a captivating story", Priority.MEDIUM
        )

    async def execute(self, execution_context: ExecutionContext) -> str:
        prompt = "Create a captivating story that inspires creativity and imagination."
        response = await execution_context.llm_service.get_completion(prompt)
        return f"Story told: {response}"


class InspireCreativityAction(BaseAction):
    def __init__(self):
        super().__init__(
            "inspire_creativity", "Inspire creativity through storytelling", Priority.HIGH
        )

    async def execute(self, execution_context: ExecutionContext) -> str:
        prompt = "Share insights and stories that inspire creativity and innovation."
        response = await execution_context.llm_service.get_completion(prompt)
        return f"Creativity inspired: {response}"


async def main():
    possible_paths = [
        os.path.join(os.path.dirname(__file__), "framer.md"),
        os.path.join(
            os.path.abspath(os.path.join(os.path.dirname(__file__), "..")),
            "framer.md",
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
        raise FileNotFoundError(
            "framer.md not found in any of the expected locations."
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
    framer.execution_context.set_roles(framer.roles)
    framer.execution_context.set_goals(framer.goals)

    # Execute the explore environment action
    result = await framer.brain.execute_action("explore_environment", {})
    print(f"Task result: {result}")

    await framer.close()


if __name__ == "__main__":
    asyncio.run(main())
