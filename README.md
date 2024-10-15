# Frame (internal)

Frame is a multi-modal cognitive agent framework designed to support fully emergent characteristics.

It consists of three main components: `Frame`, `Framed`, and `Framer`.

- **Frame**: The main interface for creating and managing [[framer|Framer]] instances. It acts as the central hub for initializing and orchestrating the various components of the framework.
- **Framer**: Represents an individual AI agent with capabilities for task management, decision-making, and interaction with language models. Each [[framer|Framer]] operates independently but can collaborate with others. By default, Framers are loaded with memory capabilities and do not include EQ modules.
- **Framed**: (plural `frameds` pronounced as frames) A collection of [[framer|Framer]] objects working together to achieve complex tasks. It enables coordination and communication between multiple [[framer|Framers]], allowing for collaborative operations asynchronously and sequentially.

This is the internal development library of Frame, that is not publicly published and contains all plugins and extensions.

## Links

(Coming soon)

[Website](https://frame.dev)
[Pip Package](https://pypi.org/project/frame-ai/)
[GitHub](https://github.com/jddunn/frame)
[API Docs](https://frame.dev/api)

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Technologies](#technologies)
4. [Architecture](#architecture)
5. [Component Hierarchy and Interactions](#component-hierarchy-and-interactions)
6. [Workflows](#workflows)
7. [Real-life Example: Research Assistant Framer](#real-life-example-research-assistant-framer)
8. [Installation](#installation)
9. [SDK Usage](#sdk-usage)
10. [CLI Usage](#cli-usage)
11. [Asynchronous and Synchronous Usage](#asynchronous-and-synchronous-usage)
12. [Future Features](#future-features)
13. [License](#license)
14. [Contributing](#contributing)
15. [Development](#development)
16. [Testing](#testing)

## Overview

Frame is a multi-modal cognitive agent framework designed to support fully emergent characteristics. It consists of three main components: `Frame`, `Framed`, and `Framer`.

- **Frame**: The main interface for creating and managing Framer instances. It acts as the central hub for initializing and orchestrating the various components of the framework.
- **Framer**: Represents an individual AI agent with capabilities for task management, decision-making, and interaction with language models. Each Framer operates independently but can collaborate with others. By default, Framers are loaded with memory capabilities and do not include EQ modules. Framers are initialized in an active state, meaning they will make decisions from new perceptions. The `act()` method starts this process, while the `halt()` method pauses it. When halted, perceptions are still registered and can be considered in future decisions unless `ignore_perceptions_while_halted` is set to True. When streaming is enabled, the `_streamed_response` variable accumulates the streamed content and resets with each new `get_completion` call.
- **Framed**: A collection of Framer objects working together to achieve complex tasks. It enables coordination and communication between multiple Framers, allowing for scalable and collaborative operations.

### Accessing Streamed Responses

When streaming is enabled, the `_streamed_response` variable in the `Framer` class accumulates the streamed content and resets with each new `get_completion` call. You can access this variable to retrieve the current status and result of the streaming operation.

The Soul component allows for setting arbitrary characteristics that influence the Framer's personality and behavior, if personality is enabled.

## Introduction

Frame is an advanced AI agent framework that enables the creation and management of cognitive agents with emergent behaviors. It is designed to be flexible, extensible, and capable of handling complex tasks and interactions.

## Features

- Multi-modal cognitive agents framework
- Supports developing dynamic, emergent behaviors
- Layered memory understanding entity relationships with Mem0
- Supports global and multi-user memory storage
- Extensible architecture with plugin engine
- Integration with popular AI APIs (OpenAI GPT, Mistral, etc.) as well as local model support
- Streaming text generation support 
- Flexible behavior and decision-making mechanics that can be based off of emotions and memories
- Monitoring and metrics; built-in LLM API usage / costs tracking

## Research Paper

Coming soon [2024](#).

## Technologies

Note: While we offer a Hugging Face adapter for local models, PyTorch and TensorFlow are not included as dependencies in the core engine. To keep the core lightweight, you will need to install the necessary plugins for local model support.

- LQML
- Hugging Face
- Mem0
- DSPy (Experimental)

## Architecture

Frame is built on a modular architecture that allows for flexible and emergent AI agent behavior. The main components of the architecture are:

- **Frame**: The main interface for creating and managing Framer instances.
- **Framer**: An AI agent with agency and soul capabilities.
- **Framed**: A group of Framer objects working together.
- **Agency**: Responsible for roles, goals, and task management.
- **Soul**: Manages memory, emotional states, and intrinsic characteristics. Characteristics can be set to arbitrary values such as 'low', 'medium', 'high', and 'extreme', influencing the personality and behavior of the Framer.
- **Brain**: Handles decision-making processes for the Framer, communicating with the Soul and Agency through the `ContextService`.
- **Mind**: Represents the cognitive processes of a Framer. It manages thoughts, decision-making processes, perceptions, and interacts with the Brain and Soul components.
- **Memory**: Manages memory storage and retrieval, supporting both global and multi-user contexts through the `MemoryService` and `Mem0Adapter`.
- **Workflow**: Manages a sequence of related tasks.
- **Task**: Represents actionable items for Framers to work on.
- **Perception**: Represents sensory input or information received by a Framer.
- **Context**: Manages roles and goals for Framers, facilitating communication between the Brain, Soul, and Agency through the `ContextService`.
- **SharedContext**: Extends Context to manage shared roles and goals across multiple Framers, enabling data sharing and collaboration through the `SharedContextService`.

### Component Hierarchy and Interactions

```
Frame
├── Framer
│   ├── Agency
│   │   ├── Roles
│   │   ├── Goals
│   │   ├── Tasks
│   │   └── Workflows
│   ├── Brain
│   │   ├── Mind
│   │   │   ├── Perceptions
│   │   │   └── Thoughts
│   │   ├── Decision
│   │   └── Memory
│   ├── Soul
│   │   ├── Emotional State
│   │   └── Core Traits
│   ├── Context
│   └── SharedContext
│       └── SharedContextService
├── Framed
│   └── Multiple Framers
├── LLM Adapters
│   ├── DSPy Adapter
│   ├── HuggingFace Adapter
│   └── LMQL Adapter
└── Services
    ├── LLMService
    ├── MemoryService
    ├── EQService
    └── ContextService
```

This updated hierarchy reflects the current structure of the Frame project, including:
- The Soul component as a separate entity within the Framer
- The addition of various Services (LLMService, MemoryService, EQService, ContextService)
- The removal of ContextService from under the Brain (it's now a separate service)
- The placement of Emotional State and Core Traits under the Soul instead of SharedContext

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
   - Tasks are executed using the `ExecutionContext`, which provides access to necessary services.
   - The `ExecutionContext` includes the LLM service, memory service, and EQ service.
   - Tasks are executed, updating the Framer's memory and potentially its emotional state.
   - Key information and experiences are stored in long-term and core memory for future use.

6. **Framed Interactions**
   - Multiple Framers can work together in a `Framed` group.
   - Framed groups can process Workflows and Tasks sequentially or in parallel.
   - Inter-Framer communication and task delegation are managed within the Framed context.

This architecture allows for a flexible, learning-capable AI agent system that can handle complex tasks while maintaining a consistent personality and improving over time. The `ExecutionContext` ensures that all necessary services are available during task execution, providing a consistent interface for actions across the system.

## Installation

### Docker

To run the Frame package using Docker, you need to build the Docker image locally. Follow these steps:

1. **Build the Docker image locally**:

   Open a terminal in the root directory of the project and run the following command to build the Docker image locally:

   ```bash
   docker build -t frame .
   ```

2. **Run the Docker container**:

   After building the image, you can run the container with:

   ```bash
   docker run -p 80:80 frame
   ```

   This will start the Frame application and expose it on port 80.

### Python

(Coming soon)

```bash
pip install frame
```

### TypeScript 

(Coming soon)

```bash
npm install frame
```

## SDK Usage

### Python

<details>
<summary>Click to expand</summary>

#### Role and Goal Generation

When initializing a Framer, the behavior for role and goal generation is as follows:

- If both roles and goals are None, they will be automatically generated using `generate_roles_and_goals()`.
- If roles is an empty list `[]` and goals is None, only roles will be generated and set.
- If goals is an empty list `[]` and roles is None, only goals will be generated and set.
- If both roles and goals are empty lists `[]`, both will be generated and set.
- If either roles or goals is provided (not None or empty list), the provided value will be used, meaning the agent will have no roles or goals.

#### Soul Seed

When creating a Framer, you can provide a soul_seed that can be either a string or a dictionary:

- If a string is provided, it will be used as the 'text' value in the soul's seed dictionary.
- If a dictionary is provided, it can include any keys and values, with an optional 'text' key for the soul's essence.

This allows for more flexible and detailed soul initialization.

#### Prompt Formatting

When using different LLM adapters, it's important to format your prompts correctly:

- For LMQL: Use triple quotes and optionally specify the expected output format.
- For DSPy: Use standard string formatting.
- For Hugging Face: Use standard string formatting.

For detailed examples and explanations, see the [Prompt Examples](docs/usage/prompt_examples.md) documentation.

```python
from frame import Frame, Framed
framer_factory = Frame()
framed_factory = Framed()

# Create a new Framer with Context and Soul Seed
context = Context()
soul_seed = {
    "text": "You are a research assistant and tutor with access to a local library of text, PDF, and image files, as well as access to online web sources like Google.",
    "specialty": "AI and machine learning",
    "experience_level": "expert"
}
research_assistant = await framer_factory.create_framer(
    context_service=context,
    soul_seed=soul_seed
)

# Add roles and goals using Context
context.set_roles([
    {
        "description": "Assist with research by searching local files and online sources",
        "name": "Research Assistant",
        "priority": 1
    },
    {
        "description": "Provide explanations and answer questions to help users learn",
        "name": "Tutor",
        "priority": 2
    }
])

context.set_goals([
    {
        "description": "Search local files and online sources, aggregate and synthesize information to present to user in a detailed report with references.",
        "name": "Information Synthesis",
        "priority": 1,
    },
    {
        "description": "Present user with relevant information from synthesized materials or own knowledge to supplement their research and inquiries. Ask and prompt users for further details to help refine their search.",
        "name": "Interactive Learning",
        "priority": 2
    }
])

# Use the sense API to get the research_assistant to do something
await research_assistant.sense(
    {
        "hear": "Please tell me the best open-source cognitive AI agent libraries in 2024."
    }
)
print(research_assistant.agency.tasks) # Will return a list with a newly created task
print(research_assistant.soul.mind.currentThought) # This would contain the result of the task when it is completed; this will have to be awaited.

# OR you can assign a task directly which will be consumed and completed in the ongoing `act()` thread
research_assistant.agency.add_task(
    {
        "description": "Please tell me the best open-source cognitive AI agent libraries in 2024.",
        "name": "research_task",
        "expected_output": "A comprehensive report of many different items with critical analysis and comparisons of the most recommended ones to use."
    }
)

# You can access the task ID after it's been added
latest_task = research_assistant.agency.tasks[-1]
print(f"Added task with ID: {latest_task.id}")

# When you're done with the Framer, make sure to close it
research_assistant.close()
```

Now, to create a framed pipeline of Framers, we can do something like this:

```python
# Create project manager framer
project_manager = await framer_factory.create_framer(
    config={
        "name": "Jane",
        "default_model": "gpt-4o"
    },
    roles=[{"name": "Project Manager"}],
    goals=[{"description": "To work collaboratively with a client to deliver project requirements, timelines, estimates, and a comprehensive plan from a idea, concept, or prompt."}],
    tasks=[
            {
                "name": "Research project idea and create plan to develop project",
                "ongoing": True, 
                "description": "Works with client and Research Assistant to research the context, niche, tools, and skills required to implement some type of project.",
                "expected_output": "Some kind of comprehensive guide / outline with timeframe and estimates in costs and what resources are needed"
            }
        ]
) 

# Create framed pipeline to allow project manager and research assistant to work together 
# to create a project plan based on research

framed_project_planner = framed_factory.create(
    framers=[
        {
            "name": "project_manager",
            "agent": project_manager,
            "weight": 70,
            "can_delegate": True # Whether agent can assign and get tasks data from other agents; defaults to True.
        },
        {
            "name": "research_assistant",
            "agent": research_assistant,
            "weight": 50, # Amount of influence / power this role should have in the group, defaults to 50,
            "can_delegate": False
        }
    ],
    # If we do not initialize a framed group with any goals, then it will create new goals for itself 
    # based on the framers' goals automatically
    goals=[],
    # By specifying an order (or flow), we imply that we are giving the project_manager agent the 
    # initial prompt, which then sends their output to a research_assistant # agent, and the 
    # research_assistant's work is sent *back* to the project_manager to produce the final output.
    order=[project_manager, research_assistant, project_manager],
    # By default sequential is set to True, and must be True if an order is specified. If it is 
    # false, then new threads will be spawned for each new agent for asynchronous processing.
    sequential=True
    # If there are no tasks specified, by default they will be created if any are necessary. You do
    # not need to send in any new tasks as we will prompt this framed # in our next line.
    tasks=[]
)

# Send a prompt to the Framed group
result = await framed_project_planner.prompt(
    "Create a project plan for an AI-powered home buying SaaS platform."
)
print("Project plan: ", result)

# When you're done with the Framed group, make sure to close all Framers
for framer in framed_project_planner.framers:
    framer.close()
```

You can do something like this to listen and check for the result of every task done in the pipeline.

```python
framed_project_planner = framed_factory.create(
    framers=[
        {
            "agent": research_assistant,
            "weight": 50
        },
        {
            "agent": project_manager,
            "weight": 70
        }
    ],
    order=[project_manager, research_assistant, project_manager],
)

# Define callback for completed tasks
def on_task_complete(framer, task):
    print(f"{framer.name} completed: {task.name}")
    print(f"Result: {task.result}")

# Run the Framed group
async def main():
    # Attach the callback to all Framers
    for framer in framed_project_planner.framers:
        framer.on_task_complete(on_task_complete)

    await framed_project_planner.prompt("Create a project plan for an AI-powered home buying SaaS platform.")

    # Clean up resources
    for framer in framed_project_planner.framers:
        framer.close()

asyncio.run(main())
```

A multi-modal Framer agent can be done like so:

```python
multi_modal_agent = await framer_factory.create_framer(
    config={
        "multi_modal_model": "gpt-4o" 
    }
)
response = await multi_modal_agent.prompt("What is this a drawing of?", images=["https://upload.wikimedia.org/wikipedia/commons/a/af/Botanical_illustration_of_Lilium_superbum.jpg"])
print(response)

# Don't forget to close the Framer when you're done
multi_modal_agent.close()
```

### Resource Cleanup

Frame uses Python's garbage collection to automatically clean up Framer resources when they are no longer in use. However, it's recommended to explicitly call the `close()` method on Framer instances when they are no longer needed, if `.act()` has been called. This ensures immediate release of resources and helps prevent any potential resource leaks.

</details>

### CLI Usage

<details>
<summary>Click to expand</summary>

The Frame CLI supports both JSON input and traditional CLI arguments for more flexible configuration. You can use it as follows:

```bash
# Using traditional CLI arguments (default behavior)
python -m frame.cli run-framer --name "Research Assistant" --model "gpt-4" --prompt "What are the best open-source AI agent libraries in 2024?"

# Using JSON input (must be explicitly specified with --json flag)
python -m frame.cli run-framer-json '{"name": "Research Assistant", "model": "gpt-4", "prompt": "What are the best open-source AI agent libraries in 2024?"}'

# Run a Framer with a perception input
python -m frame.cli run-framer-json '{"name": "Visual Analyzer", "perception": {"type": "visual", "data": {"object": "tree"}, "source": "camera"}}'

# Run a Framer with streaming output
python -m frame.cli run-framer --stream --prompt "Write a short story about an AI learning to understand human emotions"
```
When using JSON input, you can specify all Framer configuration options in a single argument. Available fields for JSON input include:
- `name`: Name of the Framer (default: "Default Framer")
- `description`: Description of the Framer
- `model`: Model to use (default: "gpt-3.5-turbo")
- `prompt`: Prompt for the Framer to respond to
- `perception`: JSON object representing a perception to process
- `soul_seed`: Optional soul seed for the Framer
- `max_len`: Maximum length for model output (default: 512)

Use `--debug` to enable debug logging.

### TUI

Frame's CLI includes a TUI (textual UI) for a interactive Terminal experience with a GUI.

```python
python -m frame.cli tui
```

</details>

## Plugins and Actions

Frame supports a powerful plugin system that allows you to extend the functionality of Framers by adding new actions. This enables you to customize the behavior of your AI agents and add domain-specific capabilities. Plugins in Frame are closely tied to the overall component architecture, interacting with various parts of the system such as the Brain, Agency, and ActionRegistry.

For a detailed overview of how plugins fit into the Frame architecture, refer to the [Component Hierarchy and Interactions](#component-hierarchy-and-interactions) section.

### Adding New Actions

To add a new action as a plugin, follow these steps:

1. **Create a New Action File**: Place your new action in the `frame/src/framer/agency/actions` directory. This file should define the logic for your action.

2. **Define the Action Function**: Implement the action logic in a function. This function should accept any necessary parameters and return the result of the action.

3. **Register the Action**: Use the `ActionRegistry` to register your action. Provide a name, the function, a description, and a priority level.

4. **Bind Variables to Action Callbacks**: When registering the action, you can bind additional variables to the action function using keyword arguments.

5. **Implement Plugin Hooks**: If your plugin needs to interact with other components or respond to specific events, implement the necessary hooks such as `on_decision_made` or `on_task_completed`.

Example of adding a new action as a plugin:

```python
# In frame/src/framer/agency/actions/weather_plugin.py
import requests

def get_weather(location, api_key, **kwargs):
    """Get weather information for a location."""
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}"
    response = requests.get(url)
    return response.json()

class WeatherPlugin:
    def __init__(self, api_key):
        self.api_key = api_key

    def register(self, action_registry):
        action_registry.register_action(
            "get_weather",
            get_weather,
            description="Get weather information for a location",
            priority=5,
            api_key=self.api_key
        )

    def on_decision_made(self, decision):
        if decision.action == "get_weather":
            print(f"Weather information requested for: {decision.parameters.get('location')}")

# Usage
from frame.src.framer.agency.action_registry import ActionRegistry

action_registry = ActionRegistry()
weather_plugin = WeatherPlugin(api_key="your_api_key_here")
weather_plugin.register(action_registry)

# The plugin is now available for use in Framers
```

In this example, we've created a WeatherPlugin that adds a `get_weather` action to the Framer. The plugin also implements an `on_decision_made` hook to respond when the action is used. This demonstrates how plugins can extend functionality and interact with the Frame system.

Plugins allow you to create modular, reusable components that can be easily added to or removed from your Frame-based AI agents, enhancing their capabilities and allowing for domain-specific customizations.

### Action Files

Each current default action is implemented in a separate file within the `actions` directory.

- `create_new_agent.py`: Handles creating a new agent with specific capabilities.
- `generate_roles_and_goals.py`: Generates roles and goals for an agent.
- `research.py`: Performs research on a given topic and summarizes findings.
- `respond.py`: Generates a response to a given input or query.
- `think.py`: Processes information and generates new thoughts or ideas.

### Observer Pattern for Plugins

The Observer Pattern is used to notify plugins of events or changes in the system. Plugins can implement the following methods to react to these events:

- `on_decision_made(decision: Decision)`: Called when a decision is made by a Framer.
- `on_task_completed(task: Task)`: Called when a task is completed by a Framer.

This allows plugins to perform additional actions or logging based on the decisions and tasks processed by Framers.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

WIP

## Development

### Testing

To run all tests, navigate to the root directory of the project and execute:

```bash
pytest
```

This command will automatically discover and run all test files in the project.

When contributing to the project, please adhere to the following guidelines for writing tests:

- Location: Place your test files in the `tests` directory.
- Naming: Follow the naming convention `test_<module>.py` for test files and `test_<function>` for test functions.
- Structure: Organize tests to mirror the structure of the source code for easy navigation.

To measure test coverage, you can use the `pytest-cov` plugin. Install it via pip if not already installed:

```bash
pip install pytest-cov
```

Run tests with coverage reporting:

```bash
pytest --cov=frame
```

This will display a coverage report in the terminal. For a more detailed report, generate an HTML report:

```bash
pytest --cov=frame --cov-report=html
```

Open the `htmlcov/index.html` file in a browser to view the coverage report.

To run a specific test file:

```bash
pytest tests/frame/src/frame/test_frame.py
```

Or a specific test in a file:

```bash
pytest tests/frame/src/frame/test_frame.py::test_get_completion
```

*Note*: Testing can take a little while as we have tests for rate limiting / retry logic, so you can exclude those (they are in the `llm_adapter` tests) if it's slow while developing others:

```python
pytest -k "not (llm_service or llm_adapter)"
```

### Documentation

The project uses plugins for MkDocs to better organize the documentation structure. The MkDocs configuration file is now located in the `docs/` folder, and the site output for HTML is also in `docs/`.

To build and serve the documentation, use the following command from the root directory:

```bash
mkdocs serve --config-file ./mkdocs.yml
```

This command will start a local server with live reloading enabled, allowing you to view changes to the documentation in real-time.

The project uses two tools for documentation:

- **MkDocs**: View the documentation at [http://localhost:3010](http://localhost:3010)
- **pdoc3**: View the API documentation at [http://localhost:3011/frame](http://localhost:3011/frame)

To serve both documentation systems simultaneously, run:

```bash
python scripts/serve_docs.py
```

This will start MkDocs on port 3010 and pdoc3 on port 3011.

#### Roam Links Converter

The project includes a `roam_links_converter.py` script in the `scripts` directory. This script is used to convert roam-style links (e.g., `[[Link Text]]`) to standard Markdown links in the documentation files. This feature allows for easier cross-referencing between documentation pages and improves the overall navigation experience.

To use the roam links converter:

1. Write your documentation using roam-style links: `[[Other Page]]`
2. Before generating the final documentation, run the converter script on your Markdown files.
3. The script will convert the roam-style links to standard Markdown links, but only if the target file exists in the documentation directory.

This approach allows for a more natural writing experience while maintaining compatibility with standard Markdown processors and static site generators.

### Using MkDocs

**Add new documentation**:
- Add new markdown files in the `docs` directory.
- Update the `mkdocs.yml` file to include the new files in the navigation.

**Build docs**:
```bash
mkdocs build
```

**Build and serve MkDocs locally**:
```bash
mkdocs serve
```

### Using pdoc3

**Generate HTML documentation**:
```bash
pdoc --html --output-dir docs_html frame
```
This command will generate HTML documentation in the `docs_html` directory.

**Serve the documentation locally**:
```bash
pdoc --http : --output-dir docs_html frame
```

### Linting

```
black .
```

### Logging

Frame uses Python's built-in logging module. To enable different logging levels:

Use the `--debug` flag when running the CLI, or, set the logging level to DEBUG in your Python code.

You can also modify the `frame/__init__.py` file to set the level for logging for the entire application.

## CI / CD

.

## Notable Contributors

- [jddunn](https://github.com/jddunn)
