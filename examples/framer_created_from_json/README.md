# Framer Created from JSON

This example demonstrates how to create a Framer instance from a JSON configuration file. The Framer is configured to perform a series of interesting tasks, showcasing its capabilities.

## How JSON Configuration Works

JSON configuration allows you to define the setup of a Framer instance using a structured and machine-readable format. Each key-value pair in the JSON file corresponds to a specific configuration aspect, such as roles, goals, or actions. This approach makes it easy to automate the configuration process and integrate with other systems.

### Structure of the JSON File

- **Keys**: Define sections like roles, goals, and actions.
- **Values**: Provide details such as role names, action descriptions, and priorities.

### Example JSON Configuration

```json
{
  "roles": [
    {
      "name": "Listener",
      "description": "Listens to audio input and transcribes it."
    }
  ],
  "goals": [
    {
      "name": "Transcribe Audio",
      "description": "Accurately transcribe audio input."
    }
  ],
  "actions": [
    {
      "name": "Record Audio",
      "description": "Record audio from the microphone.",
      "priority": "High"
    }
  ]
}
```

## Adding More Complicated Examples

To add more complex examples, you can extend the JSON configuration with additional sections or more detailed descriptions. For instance, you can define complex actions with multiple parameters or nested goals with specific conditions.

### Example of a Complex Configuration

```json
{
  "roles": [
    {
      "name": "Advanced Listener",
      "description": "Listens to audio input, transcribes it, and analyzes sentiment."
    }
  ],
  "goals": [
    {
      "name": "Analyze Sentiment",
      "description": "Determine the sentiment of transcribed audio."
    }
  ],
  "actions": [
    {
      "name": "Record and Analyze Audio",
      "description": "Record audio, transcribe it, and analyze sentiment.",
      "priority": "Critical",
      "parameters": {
        "Duration": 10,
        "SampleRate": 16000
      }
    }
  ]
}
```

## API Methods and Usage

The Framer API provides several methods to interact with the configuration and execute actions. Here are some key methods and how to use them:

### `create_framer`

Creates a new Framer instance based on the provided configuration.

```python
from frame import Frame, FramerConfig

frame = Frame()
config = FramerConfig(name="Example Framer")
framer = frame.create_framer(config)
```

### `execute_action`

Executes a specified action within the Framer.

```python
result = framer.brain.action_registry.execute_action("record_and_analyze_audio")
print(f"Action result: {result}")
```

### `add_role` and `add_goal`

Adds a new role or goal to the Framer's configuration.

```python
framer.agency.add_role({"name": "New Role", "description": "A new role description"})
framer.agency.add_goal({"name": "New Goal", "description": "A new goal description"})
```

## Why Use JSON for Configuration?

Using JSON for configuration offers several benefits:

- **Automation**: JSON is easily parsed by machines, making it ideal for automated systems.
- **Integration**: JSON is a common data format that can be easily integrated with other systems and APIs.
- **Portability**: Share configurations as simple text files that can be version-controlled and collaborated on.

## How to Run

1. Ensure you have all necessary dependencies installed.
2. Run the `main.py` script to see the Framer in action.

```bash
python main.py
```

## Exporting and Importing Configuration

This example includes functionality to export and import Framer configurations using JSON files.

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

