import sys
import os
import asyncio

# Import Frame from upper dir
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
import asyncio
from frame import Frame, FramerConfig
from frame.src.utils.config_parser import parse_json_config, parse_markdown_config

# Import Frame from upper dir
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

async def main():
    # Load configuration from JSON file
    # Try to locate the config.json file in multiple potential directories
    # Since we might be running this script inside the examples directory, 
    # or inside the root dir of the project.
    possible_paths = [
        os.path.join(os.path.dirname(__file__), 'config.json'),
        os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), 'config.json'),
        os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")), 'config.json')
    ]

    config = None
    for path in possible_paths:
        try:
            config = parse_json_config(path)
            break
        except FileNotFoundError:
            continue

    if config is None:
        raise FileNotFoundError("config.json not found in any of the expected locations.")

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
    task = {"name": "Explore", "description": "Explore the environment"}
    result = await framer.perform_task(task)
    print(f"Task result: {result}")

    # Clean up
    await framer.close()

# Run the example
if __name__ == "__main__":
    asyncio.run(main())
