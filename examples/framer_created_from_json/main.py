import os, sys
import warnings

# Suppress specific FutureWarning from torch.load
warnings.filterwarnings("ignore", category=FutureWarning, module="whisper")
import asyncio
import logging
import json

# Add the project root to the Python path to ensure all modules can be imported correctly
# If we are running the examples from the source code (not installing package from pip)
# then you need to have this line uncommented.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from frame import Frame, FramerConfig
from frame.src.utils.config_parser import parse_json_config
from frame.src.framer.brain.actions import BaseAction
from frame.src.framer.agency.priority import Priority
from frame.src.services.context.execution_context_service import ExecutionContext
from frame.src.services.llm.main import LLMService

frame = Frame()


class EngageConversationAction(BaseAction):
    def __init__(self):
        super().__init__(
            name="engage_conversation",
            description="Engage in a deep conversation",
            priority=Priority.HIGH,
        )

    async def execute(self, execution_context: ExecutionContext, **kwargs):
        prompt = "Let's have a deep conversation about the nature of consciousness and artificial intelligence."
        response = await execution_context.llm_service.get_completion(prompt)
        return f"Engaged in a deep conversation: {response}"


class TellStoryAction(BaseAction):
    def __init__(self):
        super().__init__(
            name="tell_story",
            description="Craft and narrate a captivating story",
            priority=Priority.MEDIUM,
        )

    async def execute(self, execution_context: ExecutionContext, **kwargs):
        prompt = "Create a captivating story that inspires creativity and imagination."
        response = await execution_context.llm_service.get_completion(prompt)
        return f"Story told: {response}"


class InspireCreativityAction(BaseAction):
    def __init__(self):
        super().__init__(
            name="inspire_creativity",
            description="Inspire creativity through storytelling",
            priority=Priority.HIGH,
        )

    async def execute(self, execution_context: ExecutionContext, **kwargs):
        prompt = "Share insights and stories that inspire creativity and innovation."
        response = await execution_context.llm_service.get_completion(prompt)
        return f"Creativity inspired: {response}"


async def export_config(framer, filename):
    def default_serializer(obj):
        if isinstance(obj, LLMService):
            return str(obj)  # or any other representation you prefer
        if isinstance(obj, FramerConfig):
            return obj.__dict__
        raise TypeError(
            f"Object of type {obj.__class__.__name__} is not JSON serializable"
        )

    framer_dict = framer.__dict__.copy()
    # Remove execution_context and shared_context from export
    framer_dict.pop("execution_context", None)
    framer_dict.pop("shared_context", None)
    # Remove execution_context and shared_context from export
    framer_dict.pop("execution_context", None)
    framer_dict.pop("shared_context", None)
    with open(filename, "w") as f:
        json.dump(framer_dict, f, indent=4, default=default_serializer)
    print(f"Configuration exported to {filename}")


async def import_config(filename):
    with open(filename, "r") as f:
        config_data = json.load(f)
    framer = Frame()  # Create a new Frame instance
    framer = await frame.create_framer(config=FramerConfig(**config_data))
    return framer


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

    config_data = config.__dict__ if isinstance(config, FramerConfig) else config
    # Extract actions and remove them from config_data
    action_list = config_data.pop("actions", None)

    # Create FramerConfig without the 'actions' key
    framer_config = FramerConfig(**config_data)

    # Now create the framer
    framer = await frame.create_framer(config=framer_config)

    # Register actions from the config
    if action_list:
        for action_info in action_list:
            action_name = action_info["name"]
            action_class_name = action_info.get("action_class")
            if not action_class_name:
                logger.warning(
                    f"No 'action_class' specified for action '{action_name}'. Skipping."
                )
                continue

            # Dynamically get the action class from globals()
            action_class = globals().get(action_class_name)
            if action_class is None:
                logger.error(f"Action class '{action_class_name}' not found.")
                continue

            # Create an instance of the action class
            action_instance = action_class()
            # Add the action to the action registry
            framer.brain.action_registry.add_action(action_instance)
    else:
        logger.warning("No actions found in the configuration.")

    # Execute each action and print the results
    if action_list:
        for action_info in action_list:
            action_name = action_info["name"]
            result = await framer.brain.action_registry.execute_action(action_name)
            print(f"Result of '{action_name}': {result}")
    else:
        logger.warning("No actions to execute.")

    # Export the configuration to a JSON file in the same directory as the script
    export_path = os.path.join(os.path.dirname(__file__), "exported_framer_config.json")
    await export_config(framer, export_path)

    await framer.close()


if __name__ == "__main__":
    asyncio.run(main())
