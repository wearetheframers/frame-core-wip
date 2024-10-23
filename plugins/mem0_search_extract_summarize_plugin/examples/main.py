import asyncio
import os
import sys
import os

# Import Frame from upper dir
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "..")
    )
)
from frame import Frame
from frame.src.framer.config import FramerConfig
from frame.src.framer.brain.memory.memory_adapters.mem0_adapter.concrete_mem0_adapter import (
    ConcreteMem0Adapter,
)
from plugins.mem0_search_extract_summarize_plugin.mem0_search_extract_summarize_plugin import Mem0SearchExtractSummarizePlugin


async def main():
    # Initialize Frame
    frame = Frame()

    # Create a Framer instance with the necessary permission
    config = FramerConfig(
        name="Research Assistant",
        default_model="gpt-3.5-turbo",
        permissions=[
            "with_memory",
            "with_mem0_search_extract_summarize_plugin",
            "with_shared_context",
        ],
    )
    api_key = os.getenv("MEM0_API_KEY", "your_api_key_here")
    mem0_adapter = ConcreteMem0Adapter(api_key=api_key)
    framer = await frame.create_framer(config, memory_adapter=mem0_adapter)

    # Initialize the plugin
    mem0_plugin = Mem0SearchExtractSummarizePlugin(framer)

    # Ensure the execution context is correctly set
    execution_context = framer.execution_context

    # Execute the action
    result = await mem0_plugin.execute("respond with memory retrieval", {"memory_question": "What is my favorite color?", "execution_context": execution_context})
    print(result)
    if len(sys.argv) < 2:
        print("Please provide a search query as a command line argument.")
        sys.exit(1)

    query = " ".join(sys.argv[1:])

    # Combine memory-based and non-memory-based queries
    queries = [
        {"type": "memory", "text": query},
        {"type": "non-memory", "text": "What is the capital of France?"},
        {"type": "non-memory", "text": "Explain the theory of relativity."},
        {"type": "non-memory", "text": "How does a computer work?"},
    ]

    # Shuffle the queries to mix them up
    import random

    random.shuffle(queries)

    for query in queries:
        print(f"Query: {query['text']}")
        perception = {"type": "hearing", "data": {"text": query["text"]}}
        decision = await framer.sense(perception)
        print(f"Response: {decision.reasoning}\n")


if __name__ == "__main__":
    asyncio.run(main())
