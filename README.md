# Frame

<div align="center">
  <a href="https://frame.dev">
    <img src="docs/frame-logo-transparent.png" alt="Frame Logo" width="320"/>
  </a>
  <p>Frame is a multi-modal cognitive agent framework designed to support fully emergent characteristics and efficiently automating tasks.</p>
</div>

Frame consists of three main components: `Frame`, `Framed`, and `Framer`.

- **Frame**: The main interface for creating and managing Framer instances.
- **Framer**: Represents an individual AI agent equipped with advanced capabilities for task management, decision-making, and interaction with language models. The Soul, Agency, and ExecutionContextService components are integral to a Framer's flexibility and customization, making it adaptable for a wide range of applications. These components are the primary interfaces through which users will interact with the API. The `halt()` method can be used to stop the Framer from acting, providing control over its activity.
  - Roles: Framer roles are represented by the `Role` class, which includes attributes such as id, name, description, permissions, priority, and status. Multiple roles can be active simultaneously. Roles can have different statuses (ACTIVE, INACTIVE, SUSPENDED) to reflect their current state.
  - Goals: Goals are represented by the `Goal` class, which includes attributes such as name, description, priority, and status. Multiple goals can be active at the same time, guiding the Framer's decision-making process. Goals can have different statuses (ACTIVE, COMPLETED, ABANDONED) to reflect their current state.
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
# This step is not required but is recommended to ensure that all resources are properly released.
await framer.close()
```

## Architecture

Frame is built on a modular architecture that allows for flexible and emergent AI agent behavior. The main components are:

- **Frame**: The main interface for creating and managing Framer instances.
- **Framer**: An AI agent equipped with agency and soul capabilities. The Soul and Agency components are crucial for ensuring a Framer's adaptability and customization across various scenarios. These components are the primary interfaces for user interaction with the API.
- **Framed**: A group of Framer objects working together.
- **Agency**: Manages roles, goals, and task management.
- **Soul**: Manages memory, emotional states, and intrinsic characteristics.
- **Brain**: Handles decision-making processes for the Framer.
- **Mind**: Represents the cognitive processes of a Framer.
- **Memory**: Manages memory storage and retrieval. Frame's architecture is flexible and pluggable, allowing components like memory to be swapped out. While Mem0 is designed to replace and improve upon RAG, RAG is still offered as an alternative, with the same interface but a different underlying driver.
- **Workflow**: Manages a sequence of related tasks.
- **Task**: Represents actionable items for Framers to work on.
- **Perception**: Represents sensory input or information received by a Framer.
- **Context**: Manages roles and goals for Framers.

### Component Hierarchy and Interactions

```
Frame
└── Framer
    ├── Agency
    │   ├── Roles
    │   ├── Goals
    │   ├── Tasks
    │   └── Workflows
    ├── Brain
    │   ├── Mind
    │   │   ├── Perceptions
    │   │   └── Thoughts
    │   ├── Decision
    │   └── Memory
    ├── Soul
    │   ├── Emotional State
    │   └── Core Traits
    ├── ExecutionContext
    ├── Observers
    └── ActionRegistry
Framed
└── Multiple Framers
LLM Adapters
├── DSPy Adapter
├── HuggingFace Adapter
└── LMQL Adapter
Services
├── LLMService
├── MemoryService
├── EQService
└── ExecutionContextService
```

## Usage

### SDK Usage

Frame provides a comprehensive SDK for building and managing AI agents. For detailed examples and explanations, see the [SDK Usage](docs/Usage/SDK_Usage.md) documentation.

### CLI Usage

Frame's CLI supports both JSON input and traditional CLI arguments for flexible configuration. Frame also supports a running a graphical textual user interface (TUI) in the Terminal. For more details, see the [CLI Usage](docs/CLI.md) documentation.

## Plugins and Actions

Frame supports a powerful plugin system that allows you to extend the functionality of Framers by adding new actions. For a detailed overview, refer to the [Plugins and Actions](docs/plugins.md) documentation.

## Development

### Testing

To run all tests, navigate to the root directory of the project and execute:

```bash
pytest
```

*Note*: Testing can take a little while as we have tests for rate limiting / retry logic, so you can exclude those (they are in the `llm_adapter` tests) if it's slow while developing others:

```python
pytest -k "not (llm_service or llm_adapter)"
```

### Documentation

The project uses MkDocs and can also use pdoc3 for documentation. The MkDocs config is in `docs/`, and HTML output is also in `docs/`.

To build and serve MkDocs documentation, run:

```bash
mkdocs serve --config-file ./mkdocs.yml
```

You must run the `roam_links_converter.py` script before to convert linked references to their actual paths. 

To serve both MkDocs and pdoc3 simultaneously, use the following command:

```bash
python scripts\serve_docs.py
```

If you want to skip running unit tests and only build and serve the documentation, use the `--skip-tests` argument:

```bash
python scripts\serve_docs.py --skip-tests
```

```bash
python scripts\serve_docs.py
```

This runs MkDocs on port 3010 and pdoc3 on port 3011. This script runs both with live reloading, runs unit tests on initialization and generates a coverage report, and also parses and converts link references automatically.

#### Roam Links Converter

The `roam_links_converter.py` script in `scripts` converts roam-style links (e.g., `[[Link Text]]`) to standard Markdown links. Use it before generating final docs to improve navigation.

To add a doc file to be ignored by the converter, add:

```
<!---
roam-ignore
-->
```

anywhere within the markdown file.

### Using MkDocs

**Add new documentation**:
- Add markdown files in `docs`.
- Update `mkdocs.yml` for navigation.
- API docs will be populated automatically from docstrings if you specify the class entrypoint in the markdown file.

### Commiting Without Docs

If you're developing locally with docs live reloading, you'll have doc files changed with every commit. To avoid this, you can run:

```bash
git add -- . ':!docs'
```

### Linting

Use `black` for code formatting:

```bash
black .
```

## License

This project is dual-licensed under the GNU Affero General Public License version 3 (AGPLv3) and a proprietary license. See the [LICENSE](LICENSE) file for details.

## Custom Enterprise Support

For custom enterprise support, development of features, or plugins, please contact our team at [team@frame.dev](mailto:team@frame.dev) or visit our website at [frame.dev/contact].

## Contributing

Contributions are welcome! Please see the [Contributing](docs/contributing.md) guide for more information.
