# Frame

<div align="center">
  <img src="docs/frame-logo-transparent.png" alt="Frame Logo" width="320"/>
  <p>Frame is a multi-modal cognitive agent framework designed to support fully emergent characteristics and efficiently automating tasks.</p>
</div>

Frame consists of three main components: `Frame`, `Framed`, and `Framer`.

- **Frame**: The main interface for creating and managing Framer instances.
- **Framer**: Represents an individual AI agent with capabilities for task management, decision-making, and interaction with language models.
- **Framed**: A collection of Framer objects working together to achieve complex tasks.

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Installation](#installation)
4. [Quick Start](#quick-start)
5. [Architecture](#architecture)
6. [Usage](#usage)
7. [Plugins and Actions](#plugins-and-actions)
8. [Development](#development)
9. [License](#license)
10. [Contributing](#contributing)

## Introduction

Frame is an advanced AI agent framework that enables the creation and management of cognitive agents with emergent behaviors. It is designed to be flexible, extensible, and capable of handling complex tasks and interactions.

## Features

- Multi-modal cognitive agents framework
- Supports dynamic, emergent behaviors
- Extensible architecture with plugin engine
- Integration with popular AI APIs (OpenAI GPT, Mistral, etc.)
- Streaming text generation support
- Flexible behavior and decision-making mechanics
- Monitoring and metrics; built-in LLM API usage / costs tracking

## Installation

### Docker

To run the Frame package using Docker, build the Docker image locally:

```bash
docker build -t frame .
docker run -p 80:80 frame
```

### Python

(Coming soon)

```bash
pip install frame
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

## Architecture

Frame is built on a modular architecture that allows for flexible and emergent AI agent behavior. The main components are:

- **Frame**: The main interface for creating and managing Framer instances.
- **Framer**: An AI agent with agency and soul capabilities.
- **Framed**: A group of Framer objects working together.
- **Agency**: Manages roles, goals, and task management.
- **Soul**: Manages memory, emotional states, and intrinsic characteristics.
- **Brain**: Handles decision-making processes for the Framer.
- **Mind**: Represents the cognitive processes of a Framer.
- **Memory**: Manages memory storage and retrieval.
- **Workflow**: Manages a sequence of related tasks.
- **Task**: Represents actionable items for Framers to work on.
- **Perception**: Represents sensory input or information received by a Framer.
- **Context**: Manages roles and goals for Framers.

## Usage

### SDK Usage

Frame provides a comprehensive SDK for building and managing AI agents. For detailed examples and explanations, see the [SDK Usage](docs/SDK_Usage.md) documentation.

### CLI Usage

Frame's CLI supports both JSON input and traditional CLI arguments for flexible configuration. For more details, see the [CLI Usage](docs/CLI_Usage.md) documentation.

## Plugins and Actions

Frame supports a powerful plugin system that allows you to extend the functionality of Framers by adding new actions. For a detailed overview, refer to the [Plugins and Actions](docs/plugins.md) documentation.

## Development

### Testing

To run all tests, navigate to the root directory of the project and execute:

```bash
pytest
```

### Documentation

The project uses MkDocs for documentation. To build and serve the documentation, use:

```bash
mkdocs serve
```

### Linting

Use `black` for code formatting:

```bash
black .
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please see the [Contributing](docs/contributing.md) guide for more information.
