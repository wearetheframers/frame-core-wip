# Framer Created from JSON

This example demonstrates how to create a Framer instance from a JSON configuration file. The Framer is configured to perform a series of interesting tasks, showcasing its capabilities.

## How to Run

1. Ensure you have all necessary dependencies installed.
2. Run the `main.py` script to see the Framer in action.

```bash
python main.py
```

## Exporting and Importing Configuration

This example now includes functionality to export and import Framer configurations using JSON files.

### Exporting Configuration

After running the `main.py` script, the current configuration will be exported to a file named `exported_framer_config.json`. You can change the filename in the `export_config` function if needed.

### Importing Configuration

To import a configuration from a JSON file, you can use the `import_config` function. Here’s an example of how to use it:

```python
import asyncio
from frame import Frame
from frame.src.utils.config_parser import parse_json_config
from frame.src.framer.agency.priority import Priority
from frame.src.services.context.execution_context_service import ExecutionContext

async def main():
    frame = Frame()
    config = await import_config('path_to_your_config.json')
    framer = await frame.create_framer(config)
    # Now you can use the framer as needed

if __name__ == "__main__":
    asyncio.run(main())
```

Make sure to replace `'path_to_your_config.json'` with the actual path to your JSON configuration file.
