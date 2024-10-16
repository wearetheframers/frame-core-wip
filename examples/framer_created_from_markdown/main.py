import sys
import os
import asyncio

# Import Frame from upper dir
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
import asyncio
from frame import Frame, FramerConfig
from frame.src.utils.config_parser import parse_markdown_config

async def main():
    # Load configuration from Markdown file
    # Try to locate the config.md file in multiple potential directories
    # Since we might be running this script inside the examples directory, 
    # or inside the root dir of the project.
    possible_paths = [
        os.path.join(os.path.dirname(__file__), 'config.md'),
        os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), 'config.md'),
        os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")), 'config.md')
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

    # Initialize the Frame
    frame = Frame()

    # Create a Framer instance
    if isinstance(config, FramerConfig):
        config_dict = config.__dict__
    else:
        config_dict = config

    framer = await frame.create_framer(FramerConfig(**config_dict))

    # Initialize the Framer
    await framer.initialize()

    # Simulate a task
    task = {"name": "Engage", "description": "Engage in a deep conversation"}
    result = await framer.perform_task(task)
    print(f"Task result: {result}")

    # Clean up
    await framer.close()

# Run the example
if __name__ == "__main__":
    asyncio.run(main())
