# Framer

::: frame.src.framer.Framer
    options:
      halt:
        description: "Stops the Framer from acting and processing new tasks."
      show_root_heading: false
      show_source: false
# Framer

::: frame.src.framer.framer.Framer
    options:
      show_root_heading: false
      show_source: false

## Overview

The `Framer` class represents an AI agent with cognitive capabilities. It integrates various components such as agency, brain, soul, and workflow management to create a comprehensive AI entity capable of processing perceptions, making decisions, and executing tasks.

## Key Components

Framers include several default plugins and services that are automatically available. These include:

- **Services**: `memory`, `eq`, and `shared_context` are special plugins called services. They function like plugins but do not require explicit permissions to be accessed. They are always available to Framers, enhancing their capabilities by providing essential functionalities without the need for additional permissions.

- **Default Plugin**: The `Mem0SearchExtractSummarizePlugin` is included as a default plugin. It provides a mechanism to look into memories, retrieve relevant information, and share insights, functioning as a Retrieval-Augmented Generation (RAG) mechanism. By default, all Framers inherit this action, enabling them to search, extract, and summarize information effectively. Plugins are loaded automatically during Framer creation.

### Agency

Manages roles, goals, and tasks for the Framer. 
- Roles are active by default when created, and multiple roles can be active simultaneously.
- Goals have different statuses (ACTIVE, COMPLETED, ABANDONED) which influence the Framer's decision-making process. Multiple goals can be active at the same time.

### Brain

Handles decision-making processes, integrating perceptions, memories, and thoughts. It considers the status of goals and active roles when processing perceptions and making decisions.

### Soul

Represents the core essence and personality of a Framer.

### WorkflowManager

Manages workflows and tasks.

### Emotional Intelligence

The Framer's decision-making and actions can be influenced by its emotional state if the `with_eq` permission is granted. This feature allows the Framer to simulate emotional responses, affecting how it prioritizes tasks and interacts with users. For example, a Framer in a "curious" state might prioritize exploratory actions, while one in a "calm" state might focus on routine tasks.

Provides a centralized container for various services (LLM, memory, EQ), state information, and functions needed during execution. This component ensures consistency across actions, promotes flexibility in service management, and facilitates easier testing and modular design.

## Key Methods

### `sense`

Processes a perception and makes a decision based on current goals, their statuses, and active roles.

### `prompt`

Processes a text prompt as a new perception.

### `add_plugins`

Adds multiple plugins to the Framer.

### `remove_plugins`

Removes multiple plugins from the Framer.

### `generate_tasks_from_perception`

Generates tasks based on a given perception, considering current goals, their statuses, and active roles.

## Usage

The Framer processes perceptions and makes decisions based on its current goals, active roles, and the status of each goal:

```python
framer = await Framer.create(config, llm_service)

# Process a perception
decision = await framer.sense(perception)

# Process a text prompt
decision = await framer.prompt("What is the current status of our efficiency goal?")

# Perform a task
result = await framer.perform_task(task)

# Use a plugin
plugin_result = framer.use_plugin("custom_plugin", plugin_data)
```

The Framer's decision-making process takes into account the status of each goal (ACTIVE, COMPLETED, ABANDONED) and the currently active roles, prioritizing actions that align with active goals and roles, and adapting its behavior as goals are completed or abandoned.

The plugin system allows for extensive customization and expansion of the Framer's capabilities, similar to how mods work in games. This enables developers to create a wide range of extensions and enhancements, potentially available through a plugin marketplace.
