import asyncio
import sys
from frame import Frame
from frame.src.framer.config import FramerConfig
from frame.src.plugins.search_extract_summarize_plugin import (
    SearchExtractSummarizePlugin,
)


async def main():
    # Initialize Frame
    frame = Frame()

    # Create a Framer instance
    config = FramerConfig(name="Research Assistant", default_model="gpt-3.5-turbo")
    framer = await frame.create_framer(config)

    # Initialize and register the plugin
    search_plugin = SearchExtractSummarizePlugin(framer)
    framer.register_plugin("search_extract_summarize", search_plugin)

    # Get the query from command line arguments
    if len(sys.argv) < 2:
        print("Please provide a search query as a command line argument.")
        sys.exit(1)

    query = " ".join(sys.argv[1:])

    # Use the plugin
    result = await framer.use_plugin("search_extract_summarize", query)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
