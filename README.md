# Frame: Multi-Modal Multi-Agent Cognitive Framework

<div align="center">
  <a href="https://frame.dev">
    <img src="docs/frame-logo-transparent.png" alt="Frame Logo" width="320"/>
  </a>
  <p>Frame is a multi-modal, multi-agent cognitive framework designed to support fully emergent characteristics. Framer agents are fully equipped for task automation and collaborative work.</p>
</div>

## Overview

### Actions

Actions in Frame are executable tasks that a Framer can perform. They are concrete implementations of tasks that can be executed in response to decisions made by the Framer. Actions are registered in the Framer's action registry and can be invoked directly by the Framer or through plugins. They are designed to perform specific operations, such as interacting with external systems, processing data, or executing workflows.

#### Default Actions

Frame comes with a set of default actions that are available to all Framers. These include:

- **CreateNewAgentAction**: Creates new agents within the framework.
- **GenerateRolesAndGoalsAction**: Generates roles and goals for the Framer.
- **ObserveAction**: Processes observations and generates insights or actions.
- **RespondAction**: Generates a default response based on the current context.
- **ThinkAction**: Engages in deep thinking to generate new insights or tasks.
- **ResearchAction**: Conducts research to gather information.
- **AdaptiveDecisionAction**: Makes decisions using an adaptive strategy based on context.
- **ResourceAllocationAction**: Allocates resources based on urgency, risk, and available resources.
- **ResourceAllocationAction**: Allocates resources based on urgency, risk, and available resources.

#### Default Strategies

Frame includes several strategies for decision-making:

- **ConservativeStrategy**: Favors cautious decision-making when risk is low.
- **AggressiveStrategy**: Favors quick actions when urgency is high.
- **BalancedStrategy**: Balances multiple factors for a moderate approach.
- **CollaborativeStrategy**: Focuses on collaboration when stakeholders are involved.
- **InfluentialStrategy**: Engages stakeholders based on their influence.

#### Default Plugins

Frame provides default plugins to enhance functionality:

- **Mem0SearchExtractSummarizePlugin**: Enables memory retrieval and summarization.
- **LLMService**: Provides language model services for text generation.
- **EQService**: Manages emotional intelligence aspects.
- **MemoryService**: Handles memory storage and retrieval.
- **SharedContext**: Manages shared context across components.

#### Default Permissions

Frame's default permissions are designed to ensure that Framers have access to essential services while maintaining security and control. These permissions include:

- **with_memory**: Allows access to memory services for storing and retrieving information. While Framer has access to memory by default, if you want it to respond with RAG-like features and automatically determine when to use memory retrieval versus responding without looking into any memories, you need to ensure the `with_mem0_search_extract_summarize` permission is enabled.
- **with_eq**: Enables emotional intelligence features for more nuanced interactions.
- **with_shared_context**: Provides access to shared context services for collaboration.

#### Creating New Actions

To create a new action, follow these steps:

1. Define a new class that inherits from `BaseAction`.
2. Implement the `execute` method with the action's logic.
3. Register the action with the Framer's action registry.

Example:

```python
from frame.src.framer.brain.actions.base import BaseAction
from frame.src.services import ExecutionContext

class MyCustomAction(BaseAction):
    def __init__(self):
        super().__init__("my_custom_action", "Description of the action")

    async def execute(self, execution_context: ExecutionContext, **kwargs):
        # Implement action logic here
        return {"result": "Action executed successfully"}
```

#### Execution Context

The `ExecutionContext` provides a centralized container for various services, state, and functions that actions and components might need during execution. It ensures consistent access to resources across all actions and facilitates easier testing, modular design, and state management.

Key features:
- Centralized service access: Provides access to core services like LLM, memory, and EQ.
- State management: Maintains and updates the current state of the execution.
- Goal tracking: Manages the current goals of the Framer.
- Action registry: Stores and manages available actions.

Example usage:

```python
execution_context = ExecutionContext(llm_service=llm_service)
execution_context.set_state("key", "value")
state_value = execution_context.get_state("key")
```

### Key Components

- **Frame**: The main interface for creating and managing Framer instances.

### Actions vs. Strategies

#### Actions
- **Definition**: Actions are executable tasks that a Framer can perform. They are concrete implementations of tasks that can be executed in response to decisions made by the Framer.
- **Usage**: Actions are registered in the Framer's action registry and can be invoked directly by the Framer or through plugins. They are designed to perform specific operations, such as interacting with external systems, processing data, or executing workflows.
- **Integration**: Actions are integrated into the Framer through plugins or directly within the Framer's core logic. They are prioritized and selected based on the current context, roles, goals, and perceptions.

#### Strategies
- **Definition**: Strategies are decision-making algorithms that determine how a Framer should act in a given situation. They encapsulate different approaches to decision-making, allowing the Framer to adapt its behavior based on the context.
- **Usage**: Strategies are used by the Framer to decide which actions to take. They provide a flexible mechanism for implementing different decision-making paradigms, such as conservative, aggressive, or balanced approaches.
- **Integration**: Strategies are typically implemented as part of the Framer's brain component. They can be dynamically selected and applied based on the current state and context, enabling the Framer to adapt its decision-making process.

### How Framers Use Actions and Strategies

- **Decision-Making Process**: The Framer uses strategies to evaluate the current context and determine the best course of action. This involves selecting an appropriate strategy based on factors such as urgency, risk, and available resources.
- **Action Execution**: Once a decision is made, the Framer executes the corresponding action. This involves invoking the action's logic, which may include interacting with external systems, processing data, or updating the Framer's state.
- **Plugin Interaction**: Plugins can define new actions and strategies, extending the Framer's capabilities. They can register actions with the Framer's action registry and provide custom strategies for decision-making.
- **Framer**: Represents an individual AI agent with capabilities for task management, decision-making, and interaction with language models. Each Framer operates independently but can collaborate with others.
- **Framed**: A collection of Framer objects working together to achieve complex tasks.

### Features

- Multi-modal cognitive agents framework capable of processing diverse types of perceptions
- Supports developing dynamic, emergent behaviors
- Layered memory understanding entity relationships with Mem0
- Supports global and multi-user memory storage
- Extensible architecture with plugin engine
- Integration with popular AI APIs (OpenAI GPT, Mistral, etc.) as well as local model support
- Streaming text generation support 
- Flexible behavior and decision-making mechanics that can be based off of emotions and memories
- Comprehensive priority system for roles, goals, and tasks, enabling dynamic and context-aware behavior
- Monitoring and metrics; built-in LLM API usage / costs tracking

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

### Docker

To run the Frame package using Docker, build the Docker image locally:

```bash
docker build -t frame .
```

## Quick Start

### Custom Action Registry

In the autonomous vehicle example, we demonstrate how to replace the default action registry with a custom one. This allows for a more flexible and hackable system where you can replace or extend default behaviors. The `process_perception` function takes precedence over the observe action, showing how you can customize the action registry. You can also remove actions from the Framer behavior in plugins programmatically.

Here's a simple example to get started with Frame using the synchronous wrapper `SyncFrame`:

```python
from frame.sync_frame import SyncFrame
from frame.src.framer.config import FramerConfig
from frame.src.services.llm.main import LLMService

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

- **Memory Retrieval**: The Framer retrieves personal information like favorite color, appointment details, and vacation plans from memory.
- **General Knowledge**: For questions like the capital of France, the Framer uses general knowledge without memory retrieval.
- **Decision Making**: The Framer decides whether to use memory based on the query context.

## Plugin System

Frame features a powerful and flexible plugin system inspired by game mods, allowing developers to extend the functionality of Framers. This system supports a community marketplace where plugins can be shared, sold, or given away, fostering a rich ecosystem of extensions and customizations.

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
        # Example of fetching weather data from a real API
        import requests

        api_key = "your_api_key_here"
        base_url = "http://api.weatherapi.com/v1/current.json"
        response = requests.get(base_url, params={"key": api_key, "q": location})
        data = response.json()

        if "error" in data:
            return f"Error fetching weather data: {data['error']['message']}"
        
        weather = data["current"]["condition"]["text"]
        temperature = data["current"]["temp_c"]
        return f"Weather for {location}: {weather}, {temperature}°C"
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

The Framer intelligently chooses the best decision / action to take based on the perception (in this case a user message), conversational history, assigned roles, assigned goals, soul state, and the priority levels and descriptions of the other actions.

A plugin can also remove actions from the action registry whenever a plugin is loaded (though this could result in unexpected behavior for other plugins). This can help ensure more safe and restricted behavior, or enforce specific types of behavioral flows for the Framer. An example of this is in `examples/autonomous_vehicle/`.

## Enterprise / Commerical Support

For custom enterprise support, premium plugin development, or custom development, please contact our team at [team@frame.dev](mailto:team@frame.dev) or visit our website at [frame.dev/contact](https://frame.dev/contact).

## License

This project is dual-licensed under the GNU Affero General Public License version 3 (AGPLv3) and a proprietary license. See the [LICENSE](LICENSE) file for details.

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
