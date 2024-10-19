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

# Load configuration
# Load it from the file that this script (the main.py) is in
curr_dir = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(curr_dir, "config.json")
with open(config_path, "r") as f:
    config = json.load(f)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    # Initialize Frame
    frame = Frame()

    # Create a Framer instance with the necessary permissions
    config = FramerConfig(
        name="Memory Framer",
        default_model="gpt-3.5-turbo",
        permissions=["with_memory", "with_mem0_search_extract_summarize_plugin", "with_shared_context"]
    )
    mem0_adapter = Mem0Adapter(api_key=config.get("MEM0_API_KEY"))
    memory_service = MemoryService(adapter=mem0_adapter)
    framer = await frame.create_framer(config, memory_service=memory_service, plugins=frame.plugins)

    # Store some personal memories
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
        "What is the boiling point of water in Celsius?"
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
