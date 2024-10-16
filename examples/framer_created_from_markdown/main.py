import sys
import os
import asyncio

# Import Frame from upper dir
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
import asyncio
from frame import Frame, FramerConfig
from frame.src.utils.config_parser import load_framer_from_file

async def main():
    # Load configuration from Markdown file
    config = load_framer_from_file('config.md')

    # Initialize the Frame
    frame = Frame()

    # Create a Framer instance
    framer = await frame.create_framer(config)

    # Initialize the Framer
    await framer.initialize()

    # Simulate a task
    task = {"name": "Engage", "description": "Engage in a deep conversation"}
    result = await framer.perform_task(task)
    print(f"Task result: {result}")

    # Clean up
    await frame.close()

# Run the example
if __name__ == "__main__":
    asyncio.run(main())
