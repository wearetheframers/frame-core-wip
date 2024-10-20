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
from frame.src.framer.brain.memory.memory import Memory

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

# Ensure all loggers are set to at least INFO level
for name in logging.root.manager.loggerDict:
    logging.getLogger(name).setLevel(logging.INFO)


async def main():
    # Initialize Frame
    frame = Frame()

    # Create a memory adapter
    memory_adapter = Mem0Adapter(api_key=os.environ.get("MEM0_API_KEY"))
    logger.info(f"Memory adapter created: {memory_adapter}")

    # Create a Framer instance with the necessary permissions
    config = FramerConfig(
        name="Memory Framer",
        default_model="gpt-3.5-turbo",
        permissions=[
            "with_memory",
            "with_mem0_search_extract_summarize_plugin",
            "with_shared_context",
        ],
        mem0_api_key=os.environ.get("MEM0_API_KEY"),
    )
    logger.info(f"Plugins: {frame.plugins}")
    logger.info(f"Permissions: {config.permissions}")

    framer = await frame.framer_factory.create_framer(plugins=frame.plugins)
    framer.brain.set_memory_service(MemoryService(adapter=memory_adapter))
    logger.info(f"Framer created: {framer}")
    logger.info(f"Framer brain: {framer.brain}")
    logger.info(f"Framer brain memory service: {framer.brain.memory_service}")
    logger.info(f"Framer brain memory: {framer.brain.memory}")

    mem0_plugin = Mem0SearchExtractSummarizePlugin(framer)
    logger.info(f"Mem0SearchExtractSummarizePlugin created: {mem0_plugin}")

    # Wait until the Framer is ready
    while not framer.is_ready():
        logger.warning("Framer is not ready. Retrying...")
        await asyncio.sleep(1)

    logger.info("Adding memories...")
    if framer.brain and framer.brain.memory:
        framer.brain.memory.store("My favorite color is blue.", user_id="user1")
        framer.brain.memory.store(
            "I have a dentist appointment on October 20th.", user_id="user1"
        )
        framer.brain.memory.store(
            "I plan to visit Hawaii for my vacation.", user_id="user1"
        )
        logger.info("All memories added.")
    else:
        logger.error(
            "Brain or Memory object is not initialized. Unable to store memories."
        )
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
        print(f"\nQuery: {query}")
        perception = {"type": "hearing", "data": {"text": query}}
        decision = await framer.sense(perception)
        if decision is not None:
            # Log the reasoning
            logger.info(f"Reasoning: {decision.reasoning}")

            # Execute the decision and get the result
            result = await framer.brain.execute_decision(decision)

            # Print the result of the decision
            if isinstance(result, dict):
                if "output" in result:
                    print(f"Response: {result['output']}\n")
                elif "error" in result:
                    print(f"Error: {result['error']}\n")
                elif "response" in result:
                    print(f"Response: {result['response']}\n")
                else:
                    print(f"Unexpected result format: {result}\n")
            else:
                print(f"Response: {result}\n")
        else:
            logger.warning("Decision is None, perception was queued.")


if __name__ == "__main__":
    asyncio.run(main())
