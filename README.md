# Frame: Lightweight Multi-Agent Cognitive Framework with Plugin Architecture

<div align="center">

  <a href="https://frame.dev">
    <img src="docs/frame-logo-transparent.png" alt="Frame Logo" width="320"/>
  </a>
  <div align="center" style="margin: auto">
    <!-- Placeholder links with emojis -->
    <a href="#link1" style="margin: 0 10px;">🔗 Link 1</a>
    <a href="#link2" style="margin: 0 10px;">📄 Link 2</a>
    <a href="#link3" style="margin: 0 10px;">📊 Link 3</a>
    <a href="#link4" style="margin: 0 10px;">📚 Link 4</a>
    <a href="#link5" style="margin: 0 10px;">🔍 Link 5</a>
  </div>
</div>

## Overview

Frame is a lightweight, extensible cognitive framework with a powerful plugin architecture. The core engine provides essential AI agent capabilities, while optional plugins enable advanced features like multi-modal processing, advanced memory systems, and specialized tools. This modular approach allows developers to keep their applications lightweight while having the flexibility to add capabilities as needed.

### Features

- Multi-modal cognitive agents framework capable of processing diverse types of perceptions
- Supports developing dynamic, emergent behaviors
- Layered memory understanding entity relationships with Mem0
- Supports global and multi-user memory storage
- Extensible architecture with plugin engine allowing for limitless modifications
- Integration with popular AI APIs (OpenAI GPT, Mistral, etc.) as well as local model support
- Streaming text generation support 
- Flexible behavior and decision-making mechanics that can be based off of emotions and memories
- Comprehensive priority system for roles, goals, and tasks, enabling dynamic and context-aware behavior
- Monitoring and metrics; built-in LLM API usage / costs tracking
- Dynamic validation of variables and parameters in decision-making processes to enhance reliability and prevent execution errors.

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
    │   └── Plugins
    ├── Soul
    │   ├── Emotional State
    │   └── Core Traits
    ├── Context
    ├── Observers
    └── Action Registry
Framed
└── Multiple Framers
Services
├── LLM Service
│   └── LLM Adapters
│       └── DSPy Adapter
│       └── HuggingFace Adapter
│       └── LMQL Adapter
├── Memory Service
│   └── Memory Adapters
│       └── Mem0 Adapter
├── EQ Service
└── Context Service
│   └── Execution Context
│   └── Local Context
│   └── Shared Context
```

## Agent Flow

1. **Framer Creation and Initialization**
   - A `Frame` instance creates one or more `Framer` agents.
   - Each `Framer` is initialized with a `Soul` (including a seed story) and an `Agency`.
   - The `Agency` generates roles and goals based on the seed story if not provided.

2. **Perception and Thought Process**
   - The `Framer` receives perceptions through the `sense()` method.
   - Perceptions are processed in the `Soul` and stored in short-term memory.
   - The `Mind` generates new thoughts based on perceptions and memories.

3. **Decision Making**
   - The `Brain` component makes decisions based on current perceptions, memories, and thoughts.
   - **New:** Variables and parameters are validated during decision-making to ensure actions can be executed properly.
   - The `Brain` component makes decisions based on current perceptions, memories, and thoughts.
   - Decisions can lead to actions, new task generation, or changes in the Framer's state.

4. **Workflow and Task Management**
   - Based on the Brain's decisions, the `Agency` may create Workflows and Tasks.
   - The `Agency` manages task prioritization and execution within each Workflow.

5. **Task Execution and Learning**
   - Tasks are executed, updating the Framer's memory and potentially its emotional state.
   - Key information and experiences are stored in long-term and core memory for future use.

6. **Framed Interactions**
   - Multiple Framers can work together in a `Framed` group.
   - Framed groups can process Workflows and Tasks sequentially or in parallel.
   - Inter-Framer communication and task delegation are managed within the Framed context.

## Installation

### Local Development

For local development, clone the repository and install in editable mode with development dependencies:

```bash
git clone https://github.com/yourusername/frame.git
cd frame
pip install -e ".[dev]"
```

This will install all development dependencies including testing and documentation tools.

### Installing Plugins

Frame supports several plugin types that can be installed separately:

```bash
# Install all available plugins
pip install -e ".[all-plugins]"

# Or install specific plugins
pip install frame-ai-plugin-audio  # Audio processing
pip install frame-ai-plugin-local-inference  # Local LLM support
pip install frame-ai-plugin-vector-store  # Vector storage
pip install frame-ai-plugin-dspy  # DSPy integration
pip install frame-ai-plugin-memory  # Advanced memory systems
```

### Local LLM Setup

To use local LLMs, you'll need to:

1. Install the local inference plugin:
```bash
pip install frame-ai-plugin-local-inference
```

2. Install supported model backends:
```bash
# For CPU inference
pip install llama-cpp-python

# For CUDA GPU support
pip install llama-cpp-python --prefer-binary --extra-index-url=https://jllllll.github.io/llama-cpp-python-cuBLAS-wheels/AVX2/cu118
```

3. Download model weights:
- Place your GGUF format models in `~/.frame/models/`
- Supported models include:
  - Mistral-7B-v0.1.Q4_K_M
  - Llama-2-7b-chat.Q4_K_M
  - Neural-Chat-7B-v3-1.Q4_K_M
  - And other GGUF format models

4. Configure model paths in your code:
```python
from frame import Frame
from frame.framer.config import FramerConfig

frame = Frame(
    default_model="local://~/.frame/models/mistral-7b-v0.1.Q4_K_M.gguf",
    model_config={
        "context_length": 4096,
        "gpu_layers": 0  # Set to higher number to use GPU
    }
)
```

### Docker

To run the Frame package using Docker, build the Docker image locally:

```bash
docker build -t frame .
```

## Quick Start

### Simple

Here's a simple example to get started with Frame using the synchronous wrapper `SyncFrame`:

```python
from frame.sync_frame import SyncFrame
from frame.framer.config import FramerConfig
from frame.services.llm.main import LLMService

# Initialize SyncFrame with an LLMService
llm_service = LLMService(api_key="your_api_key")
sync_frame = SyncFrame(llm_service=llm_service)

# Create a Framer instance
config = FramerConfig(name="Example Framer", default_model="gpt-4o-mini")
framer = sync_frame.create_framer(config)

# Define a task
task = {"description": "Engage in a deep conversation"}
result = sync_frame.perform_task(framer, task)
print(f"Task result: {result}")

# Clean up
sync_frame.close_framer(framer)
```

## Chatbot Interaction Example

This example demonstrates how to interact with Frame like a chatbot using both the `prompt` method and the `sense` method with a perception of hearing. Both methods achieve the same result.

```python
import asyncio
from frame import Frame
from frame.framer.config import FramerConfig

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

Both methods allow you to interact with Frame as if it were a chatbot, providing flexibility in how you choose to send input.

## Memory Retrieval Example

This example demonstrates how Frame can retrieve information from memory and distinguish between responses that require memory and those that do not. Framer will automatically choose between responding from RAG-like memory augmentation versus a regular response without memory automatically, provided the `with_memory` and `with_mem0_search_extract_summarize_plugin` plugins are provided to a Framer (which are included by default in Frame's package). The Framer takes *no* additional API calls to an LLM service to distinguish between which response type it should pick.

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
    if framer.brain and framer.brain.memory:
        framer.brain.memory.store("My favorite color is blue.", user_id="user1")
        framer.brain.memory.store("I have a dentist appointment on October 20th.", user_id="user1")
        framer.brain.memory.store("I plan to visit Hawaii for my vacation.", user_id="user1")
    else:
        print("Brain or Memory service is not initialized. Unable to store memories.")

    # Queries
    queries = [
        "What is my favorite color?", # Framer considers this question for memory retrieval
        "When is my next appointment?", # Framer considers this question for memory retrieval
        "What are my vacation plans?", # Framer considers this question for memory retrieval
        "What is the capital of France?" # Framer considers this question as general knowledge it knows
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

## Actions / Plugins

Frame features a powerful and flexible plugin system inspired by game mods, allowing developers to extend the functionality of Framers. This system supports a community marketplace where plugins can be shared, sold, or given away, fostering a rich ecosystem of extensions and customizations.

### Plugin Types

1. **Core Plugins** (included in base package):
   - Basic memory management
   - Simple text generation
   - Core decision making

2. **Official Plugins**:
   - Audio Processing (`frame-ai-plugin-audio`)
   - Local LLM Inference (`frame-ai-plugin-local-inference`)
   - Vector Store (`frame-ai-plugin-vector-store`)
   - DSPy Integration (`frame-ai-plugin-dspy`)
   - Advanced Memory (`frame-ai-plugin-memory`)

3. **Community Plugins**:
   - Available through PyPI
   - Can be installed via pip

### Plugin Configuration

Plugins can be configured when creating a Frame instance:

```python
frame = Frame(
    plugins_dir="/path/to/custom/plugins",
    plugin_config={
        "audio": {
            "default_device": 0,
            "sample_rate": 44100
        },
        "local_inference": {
            "model_path": "~/.frame/models/mistral-7b.gguf",
            "gpu_layers": 35
        }
    }
)
```

### Plugin Permissions

Plugins require explicit permissions to be activated:

```python
config = FramerConfig(
    name="PluginEnabledFramer",
    permissions=[
        "with_memory",
        "with_audio",
        "with_local_inference",
        "with_vector_store"
    ]
)
framer = await frame.create_framer(config)
```

For more detailed information on creating and using plugins, please refer to the [Plugins and Actions documentation](docs/plugins.md).

## Enterprise / Commerical Support

For custom enterprise support, premium plugin development, or custom development, please contact our team at [team@frame.dev](mailto:team@frame.dev) or visit our website at [frame.dev/contact](https://frame.dev/contact).

## License

This project is dual-licensed under the GNU Affero General Public License version 3 (AGPLv3) and a custom proprietary license for certain enterprise use cases. See the [LICENSE](LICENSE) file for details.

## Development

### Testing

To run all tests, navigate to the root directory of the project and execute:

```bash
pytest
```

*Note*: Testing can take a little while as we have tests for rate limiting / retry logic, so you can exclude those (they are in the `llm_adapter` tests) if it's slow while developing others:

```bash
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

This runs MkDocs on port 3010 and pdoc3 on port 3011. This script runs both with live reloading, runs unit tests on initialization and generates a coverage report, and also parses and converts link references automatically. Add `--skip-tests` to skip tests when started.

#### Roam Links Converter

The `roam_links_converter.py` script in `scripts` converts roam-style links (e.g., `[[Link Text]]`) to standard Markdown links. Use it before generating final docs to improve navigation.

To add a doc file to be ignored by the converter, add this anywhere in the markdown file:

```
<!---
roam-ignore
-->
```

#### Commiting Without Docs

If you're developing locally with docs live reloading, you'll have doc files changed with every commit. To avoid this, you can run:

```bash
git add -- . ':!docs'
```

### Linting

```bash
black .
```

## License

This project is dual-licensed under the GNU Affero General Public License version 3 (AGPLv3) and a proprietary license. See the [LICENSE](LICENSE) file for details.

## Custom Enterprise Support

For custom enterprise support, development of features, or plugins, please contact our team at [team@frame.dev](mailto:team@frame.dev) or visit our website at [frame.dev/contact].

## Contributing

Contributions are welcome! Please see the [Contributing](docs/contributing.md) guide for more information.
