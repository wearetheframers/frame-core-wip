import asyncio
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from frame import Frame
from frame.src.framer.config import FramerConfig
import json
from frame.src.framer.brain.memory.memory_adapters.mem0_adapter import Mem0Adapter

# Load configuration
with open("config.json", "r") as f:
    config = json.load(f)

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
    framer = await frame.create_framer(config, memory_adapter=mem0_adapter)

    # Store some personal memories
    framer.memory_service.store("My favorite color is blue.", user_id="user1")
    framer.memory_service.store("I have a dentist appointment on October 20th.", user_id="user1")
    framer.memory_service.store("I plan to visit Hawaii for my vacation.", user_id="user1")

    # Query the Framer for personal details
    queries = [
        "What is my favorite color?",
        "When is my next appointment?",
        "What did I say about my vacation plans?"
    ]

    for query in queries:
        print(f"Query: {query}")
        result = await framer.use_plugin_action("mem0_search_extract_summarize_plugin", "mem0_search_extract_summarize", {"query": query, "user_id": "user1"})
        print(f"Response: {result}\n")

if __name__ == "__main__":
    asyncio.run(main())
