import asyncio
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from frame import Frame
from frame.src.framer.config import FramerConfig
import json
import random
import logging
from frame.src.framer.brain.memory.memory_adapters.mem0_adapter import Mem0Adapter
from frame.src.services.memory.main import MemoryService

from frame.src.plugins.mem0_search_extract_summarize_plugin.mem0_search_extract_summarize_plugin import (
    Mem0SearchExtractSummarizePlugin,
)

# Load configuration
# Load it from the file that this script (the main.py) is in
curr_dir = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(curr_dir, "config.json")
with open(config_path, "r") as f:
    config = json.load(f)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def main():
    # Initialize Frame
    frame = Frame()

    # Create a Framer instance with the necessary permissions
    config = FramerConfig(
        name="Memory Framer",
        default_model="gpt-3.5-turbo",
        permissions=[
            "with_memory",
            "with_mem0_search_extract_summarize_plugin",
            "with_shared_context",
        ],
    )
    mem0_adapter = Mem0Adapter(api_key=config.get("MEM0_API_KEY"))
    memory_service = MemoryService(adapter=mem0_adapter)
    print("Memory service created: ", memory_service)
    print("Plugins: ", frame.plugins)
    print("Permissions: ", config.permissions)
    framer = await frame.framer_factory.create_framer(
        memory_service=memory_service, plugins=frame.plugins
    )
    mem0_plugin = Mem0SearchExtractSummarizePlugin(framer)

    # framer.brain.agency.action_registry.add_action(
    #     "respond with memory retrieval",
    #     description="This action is ideal for responding to personal questions that involve historical or memory-based "
    #                 "information about the user or the Framer. It leverages the Framer's memory to retrieve relevant data "
    #                 "or previously saved texts, providing comprehensive answers or insights based on stored memories. "
    #                 "When questions reference or relate to past conversations, this action is preferred. It generally "
    #                 "takes precedence over `think` and `observe` actions, especially for questions. If uncertain whether "
    #                 "a question can be answered with or without memory, default to this action.",
    #     action_func=mem0_plugin.mem0_search_extract_summarize,
    #     priority=8,
    # )

    # Wait until the Framer is ready
    while not framer.is_ready():
        logger.warning("Framer is not ready. Retrying...")
        await asyncio.sleep(1)
    print("Adding memories..")
    print("\t- My favorite color is blue.")
    print("\t- I have a dentist appointment on October 20th.")
    print("\t- I plan to visit Hawaii for my vacation.")
    # framer.memory_service.store("My favorite color is blue.", user_id="user1")
    # framer.memory_service.store("I have a dentist appointment on October 20th.", user_id="user1")
    # framer.memory_service.store("I plan to visit Hawaii for my vacation.", user_id="user1")
    print("All memories added.")
    # Query the Framer for personal details
    queries = [
        "What is my favorite color?",
        "When is my next appointment?",
        "What did I say about my vacation plans?",
        "What is the capital of France?",
        "How many continents are there?",
        "What is the boiling point of water in Celsius?",
    ]

    random.shuffle(queries)
    for query in queries:
        print(f"Query: {query}")
        perception = {"type": "hearing", "data": {"text": query}}
        decision = await framer.sense(perception)
        if decision is not None:
            # Log the reasoning
            logger.info(f"Reasoning: {decision.reasoning}")

            # Execute the decision and get the result
            result = await framer.agency.execute_decision(decision)

            # Print the result of the decision
            print(f"Response: {result}\n")
        else:
            logger.warning("Decision is None, perception was queued.")


if __name__ == "__main__":
    asyncio.run(main())
