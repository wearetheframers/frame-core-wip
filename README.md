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
- Extensible architecture with plugin engine
- Integration with popular AI APIs (OpenAI GPT, Mistral, etc.)
- Streaming text generation support
- Flexible behavior and decision-making mechanics
- Monitoring and metrics; built-in LLM API usage / costs tracking

## Plugins and Extensions

Frame supports a powerful plugin system that allows you to extend the functionality of Framers by adding new actions. Inspired by game mods, this system offers unlimited potential for extensions, with automatic conflict resolution and a community marketplace for plugins. This fosters a rich ecosystem of extensions and customizations.

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

## Advanced Examples

### Chatbot Interaction Example

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

### Explanation

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

## Enterprise / Commerical Support

For custom enterprise support, premium plugin development, or custom development, please contact our team at [team@frame.dev](mailto:team@frame.dev) or visit our website at [frame.dev/contact](https://frame.dev/contact).

## License

This project is dual-licensed under the GNU Affero General Public License version 3 (AGPLv3) and a proprietary license. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please see the [Contributing](docs/contributing.md) guide for more information.
