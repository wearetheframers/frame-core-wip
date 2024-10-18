import asyncio
import os
import sys
import os
# Import Frame from upper dir
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "..")))
from frame import Frame
from frame.src.framer.config import FramerConfig
from frame.src.framer.brain.memory.memory_adapters.mem0_adapter.concrete_mem0_adapter import ConcreteMem0Adapter


async def main():
    # Initialize Frame
    frame = Frame()

    # Create a Framer instance with the necessary permission
    config = FramerConfig(
        name="Research Assistant",
        default_model="gpt-3.5-turbo",
        permissions=["with_memory", "with_mem0_search_extract_summarize_plugin", "with_shared_context"]
    )
    api_key = os.getenv("MEM0_API_KEY", "your_api_key_here")
    mem0_adapter = ConcreteMem0Adapter(api_key=api_key)
    framer = await frame.create_framer(config, memory_adapter=mem0_adapter)

    # Get the query from command line arguments
    if len(sys.argv) < 2:
        print("Please provide a search query as a command line argument.")
        sys.exit(1)

    query = " ".join(sys.argv[1:])

    # Use the plugin
    result = await framer.use_plugin_action("mem0_search_extract_summarize_plugin", "mem0_search_extract_summarize", {"query": query})
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
