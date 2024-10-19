# Frame

<div align="center">
  <a href="https://frame.dev">
    <img src="docs/frame-logo-transparent.png" alt="Frame Logo" width="320"/>
  </a>
  <p>Frame is a multi-modal multi-agent framework designed to support fully emergent characteristics and efficiently automate tasks, with an extensible plugin architecture inspired by game mods.</p>
</div>

## Overview

Frame is an advanced AI agent framework that enables the creation and management of cognitive agents with emergent behaviors. It is designed to be flexible, extensible, and capable of handling complex tasks and interactions.

### Key Components

- **Frame**: The main interface for creating and managing Framer instances.
- **Framer**: Represents an individual AI agent equipped with advanced capabilities for task management, decision-making, and interaction with language models.
- **Framed**: A collection of Framer objects working together to achieve complex tasks.

### Features

- Multi-modal cognitive agents framework
- Supports dynamic, emergent behaviors
- Extensible architecture with plugin engine inspired by game mods
- Integration with popular AI APIs (OpenAI GPT, Mistral, etc.)
- Streaming text generation support
- Flexible behavior and decision-making mechanics
- Emotional intelligence and state (optional)
- Monitoring and metrics; built-in LLM API usage / costs tracking
- Synchronous wrapper provided around async functions

## Installation

### Docker

To run the Frame package using Docker, build the Docker image locally:

```bash
docker build -t frame .
```

## Quick Start

Here's a simple example to get started with Frame:

```python
from frame import Frame, FramerConfig

# Initialize Frame
frame = Frame()

# Create a Framer instance
config = FramerConfig(name="Example Framer", default_model="gpt-4o-mini")
framer = await frame.create_framer(config)

# Define a task
task = {"name": "Engage", "description": "Engage in a deep conversation"}
result = await framer.perform_task(task)
print(f"Task result: {result}")

# Clean up
await framer.close()
```

## Chatbot Interaction Example

This example demonstrates how to interact with Frame like a chatbot using both the `prompt` method and the `sense` method with a perception of hearing. Both methods achieve the same result.

```python
import asyncio
from frame import Frame, FramerConfig

async def main():
    # Initialize Frame
    frame = Frame()

    # Create a Framer instance
    config = FramerConfig(name="Chatbot Framer", default_model="gpt-4o-mini")
    framer = await frame.create_framer(config)

    # Using the prompt method
    response = await framer.prompt("Hello, how are you?")
    print(f"Response using prompt: {response}")

    # Using the sense method with a perception of hearing
    perception = {"type": "hearing", "data": {"text": "Hello, how are you?"}}
    decision = await framer.sense(perception)
    if decision:
        response = await framer.agency.execute_decision(decision)
        print(f"Response using sense: {response}")

    await framer.close()

asyncio.run(main())
```

- **Prompt Method**: Directly sends a text prompt to the Framer and receives a response.
- **Sense Method**: Sends a perception of hearing to the Framer, which processes it and makes a decision to respond.

Both methods allow you to interact with Frame as if it were a chatbot, providing flexibility in how you choose to send input.

### Memory Retrieval Example

This example demonstrates how Frame can retrieve information from memory and distinguish between responses that require memory and those that do not.

```python
import asyncio
from frame import Frame, FramerConfig

async def main():
    # Initialize Frame
    frame = Frame()

    # Create a Framer instance with memory permissions
    config = FramerConfig(
        name="Memory Framer",
        default_model="gpt-4o-mini",
        permissions=["with_memory", "with_mem0_search_extract_summarize_plugin"]
    )
    framer = await frame.create_framer(config)

    # Add memories
    framer.memory_service.store("My favorite color is blue.", user_id="user1")
    framer.memory_service.store("I have a dentist appointment on October 20th.", user_id="user1")

    # Queries
    queries = [
        "What is my favorite color?",
        "When is my next appointment?",
        "What is the capital of France?"
    ]

    for query in queries:
        perception = {"type": "hearing", "data": {"text": query}}
        decision = await framer.sense(perception)
        if decision:
            result = await framer.agency.execute_decision(decision)
            print(f"Query: {query}\nResponse: {result}\n")

    await framer.close()

asyncio.run(main())
```

- **Memory Retrieval**: The Framer retrieves personal information like favorite color and appointment details from memory.
- **General Knowledge**: For questions like the capital of France, the Framer uses general knowledge without memory retrieval.
- **Decision Making**: The Framer decides whether to use memory based on the query context.

## Plugin System

Frame features a powerful and flexible plugin system inspired by game mods, allowing developers to extend the functionality of Framers. This system supports a community marketplace where plugins can be shared, sold, or given away, fostering a rich ecosystem of extensions and customizations.

### Key Features

- **Easy and Flexible API**: Develop plugins using a straightforward API. Plugins can be Python packages imported into Framer or stored in a local directory for Frame to ingest.
- **Community Marketplace**: Share and discover plugins in a community-driven marketplace, similar to mod communities in popular games.

### Example: Weather Forecast Plugin

Here's an example of how to develop, import, and run a plugin that provides weather forecasts:

1. **Create the Plugin**: Define a new plugin class in a Python file, e.g., `weather_plugin.py`.

```python
from frame.src.framer.brain.plugins.base import BasePlugin
from typing import Any, Dict

class WeatherPlugin(BasePlugin):
    async def on_load(self):
        self.add_action("get_weather", self.get_weather, "Fetch weather information for a location")

    async def execute(self, action: str, params: Dict[str, Any]) -> Any:
        if action == "get_weather":
            # Use the parse_location function to extract the location from natural language
            location = await self.parse_location(params.get("prompt"))
            return await self.get_weather(location)
        else:
            raise ValueError(f"Unknown action: {action}")

    async def parse_location(self, prompt: str) -> str:
        # Use Frame's get_completion method with LMQL prompt templating to parse location
        formatted_prompt = format_lmql_prompt(prompt, expected_output="location")
        response = await self.framer.get_completion(formatted_prompt)
        return response.strip()

    async def get_weather(self, location: str) -> str:
        # Simulate fetching weather data
        return f"Weather for {location}: Sunny, 25°C"
```

2. **Register the Plugin**: Import and register the plugin with a Framer instance.

```python
from frame import Frame, FramerConfig
from weather_plugin import WeatherPlugin

async def main():
    frame = Frame()
    config = FramerConfig(name="WeatherFramer", default_model="gpt-4o-mini")
    framer = await frame.create_framer(config)

    # Register the plugin
    weather_plugin = WeatherPlugin(framer)
    framer.plugins["weather_plugin"] = weather_plugin

    # Register the plugin
    weather_plugin = WeatherPlugin(framer)
    framer.plugins["weather_plugin"] = weather_plugin

    # Use the plugin with a prompt
    response = await framer.prompt("How's the weather today in NY?")
    print(f"Response using prompt: {response}")

    # Use the plugin with a sense method
    perception = {"type": "thought", "data": {"text": "I want to know what the weather is like in New York today since I am going there later."}}
    # Framer's decision making should prompt it to fetch the weather for the location
    decision = await framer.sense(perception)
    if decision:
        response = await framer.agency.execute_decision(decision)
        print(f"Response using sense: {response}")

    await framer.close()

asyncio.run(main())
```

This example demonstrates how to create a plugin that fetches weather information for a specific location if given, register it with a Framer, and execute its actions, all in natural conversation.

## Enterprise / Commerical Support

For custom enterprise support, premium plugin development, or custom development, please contact our team at [team@frame.dev](mailto:team@frame.dev) or visit our website at [frame.dev/contact](https://frame.dev/contact).

## License

This project is dual-licensed under the GNU Affero General Public License version 3 (AGPLv3) and a proprietary license. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please see the [Contributing](docs/contributing.md) guide for more information.
