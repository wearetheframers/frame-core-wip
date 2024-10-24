---
title: Framer
weight: 20
---

# Framer Architecture

## Overview

The Framer class represents an individual AI agent within the Frame cognitive agent framework. It serves as the core component, enabling the creation and management of intelligent agents with capabilities for perception processing, task management, decision-making, and interaction with language models. Framers are designed to exhibit emergent behaviors and can be customized for various applications.

### Attributes

- `config` (FramerConfig): Configuration settings for the Framer.
- `llm_service` (LLMService): The language model service to be used by the Framer.
- `context_service` (Optional[ContextService]): Service for managing context. Default is None.
- `memory_service` (Optional[MemoryService]): Service for managing memory. Default is None.
- `soul_seed` (Optional[Dict[str, Any]]): Initial seed for the Framer's soul. Default is None.
- `_streamed_response` (dict): A dictionary with keys `status` and `result` that accumulates streamed content when `get_completion` is called with streaming enabled. Resets with each new call.
- `plugins` (Dict[str, Any]): A dictionary of loaded plugins that extend the Framer's capabilities.
- `permissions` (List[str]): A list of permissions that determine which plugins and services the Framer can access.

### Key Features

Framers include several default plugins and services that are automatically available. These include:

- **Services**: `memory`, `eq`, and `shared_context` are special plugins called services. They function like plugins but do not require explicit permissions to be accessed. They are always available to Framers, enhancing their capabilities by providing essential functionalities without the need for additional permissions.

- **Default Plugin**: The `Mem0SearchExtractSummarizePlugin` is included as a default plugin. It provides a response mechanism that requires memory retrieval, functioning as a Retrieval-Augmented Generation (RAG) mechanism. By default, all Framers inherit this action, enabling them to search, extract, and summarize information effectively.

- **Perception Processing**: Framers can sense and process various types of incoming data (perceptions) such as text, images, and sounds, provided the appropriate plugins and inputs are available.
- **Decision Making**: Based on incoming perceptions, roles, goals, available plugins, and permissions, Framers make decisions on what actions to take.
- **Action Execution**: Framers can perform actions based on their decisions, including creating tasks and workflows.
- **Plugin Integration**: Framers can use plugins to extend their behavior with new actions. When a plugin action is well-described, the Framer can make reasonable moves to take that action based on context, internal thinking, and the action's priority compared to other possible actions.

Framer's plugins architecture means that when Frame is instantiated, it spends time loading plugins, which could be hundreds or thousands, and take a while to load. Framer has an `acting` property to see if it's ready and whether all plugins have loaded or not, called `plugin_loading_complete` and `plugin_loading_progress`. Because of this, users should be aware before adding too many plugins. However, Framer does queue perceptions/interactions to the agent and processes the queue when it is ready, if requests are made before it is ready. So it is not necessary to handle this in your code, but it could result in delays on startup.
- **Permission-Based Execution**: Framers require explicit permissions for all plugins. Users must add all permissions for any plugins they want to use, ensuring Framers only use plugins and services they have access to.

## Related Components

- [[agency]]: Manages roles, goals, tasks, and workflows for Framers.
- [[brain]]: Handles decision-making processes, integrating perceptions, memories, and thoughts.
- [[soul]]: Represents the core essence and personality of a Framer.
- [[mind]]: Represents the cognitive processes of a Framer.
- [[execution_context_service]]: Provides a shared context for executing actions across different components of a Framer.

## Initialization and Key Features

### Initialization

Framers start acting immediately upon creation, processing perceptions and making decisions. If you need to stop the `Framer` from acting or making new tasks, use the `halt()` method. The `halt()` method is crucial for pausing the Framer's activities without shutting it down completely.

- Task Management: Create and manage tasks efficiently.
- Decision Making: Utilize advanced decision-making processes to guide actions.
- Language Model Interaction: Interact with various language models for generating responses and performing tasks. Note: DSPy does not support streaming mode.
- Perception Processing: Handle and respond to various types of input (text, visual, audio, etc.).
- Memory Management: Store and retrieve information for long-term learning and context awareness. Frame's architecture is flexible and pluggable, allowing components like memory to be swapped out. Mem0 is designed to replace and improve upon RAG, but RAG is still offered as an alternative, maintaining the same interface with a different underlying driver.
- Multi-modal Support: Process and generate responses in multiple modalities.
- Emotional Intelligence: Simulate emotional states and responses (work in progress).
- Flexible Behavior: Adapt behavior based on roles, goals, and context.
- Plugin Support: Extend functionality through custom plugins.
- Automatic Role and Goal Generation: If roles or goals are not provided during initialization, they will be automatically generated:
  - If both roles and goals are None, they will be generated using `generate_roles_and_goals()`.
  - If roles is an empty list `[]`, no roles or goals will be assigned, as the Framer has no roles to base goals on.
  - If goals is an empty list `[]` and roles is None, roles will be generated and goals will be generated based on these roles.
  - If both roles and goals are empty lists `[]`, both will be generated.
  - If roles are None or an empty list and goals are provided, roles will be generated and new goals will be added to the existing ones.
  - If either roles or goals is provided (not None or empty list), the provided value will be used.

## Advanced Features

### Memory Management

Framers use the Mem0 system for complex memory management, allowing them to store and retrieve information across multiple interactions. This enables long-term learning and context-aware decision-making.

```python
# Accessing and updating memory
memory_entry = framer.brain.memory.get("important_concept")
framer.brain.memory.store("new_information", "This is a new piece of information")
```

### Plugin System

Framers support a robust plugin system, allowing for extensive customization and expansion of capabilities. This system is designed to be as flexible and powerful as mods in games, enabling developers to create a wide range of extensions and enhancements.

```python
# Example of using a plugin
from frame.plugins import CustomPlugin

framer.add_plugin(CustomPlugin())
result = framer.use_plugin("custom_plugin", some_data)
```

### Emotional Intelligence

The Soul component of a Framer can be configured to simulate emotional states and responses. This feature is still in development and will allow for more nuanced and human-like interactions.

```python
# Setting emotional characteristics (future feature)
framer.soul.set_emotional_trait("empathy", "high")
framer.soul.set_emotional_state("curiosity", 0.8)
```

### Plugin Support

Framers support plugins to extend their functionality. Plugins can be developed to add new capabilities or integrate with external systems.

```python
# Example of using a hypothetical plugin (implementation may vary)
from frame.plugins import ImageAnalysisPlugin

framer.add_plugin(ImageAnalysisPlugin())
image_analysis_result = framer.use_plugin("image_analysis", image_data)
```

# Example of Framer initialization with empty roles
framer_with_no_roles = await framer_factory.create_framer(
    config=FramerConfig(name="EmptyRolesFramer"),
    roles=[]
)
print(framer_with_no_roles.agency.roles)  # Output: []
print(framer_with_no_roles.agency.goals)  # Output: []

## Best Practices

1. **Configure Appropriately**: Carefully define roles, goals, and the soul seed to shape the Framer's behavior effectively. Be aware that initializing a Framer with an empty list of roles will result in no goals being assigned.
2. **Use Multi-modal Inputs**: Leverage the Framer's ability to process various types of inputs for more comprehensive understanding.
3. **Manage Memory**: Utilize the memory system to maintain context and improve the Framer's performance over time.
4. **Monitor and Adjust**: Regularly review the Framer's performance and adjust its configuration as needed.
5. **Leverage Plugins**: Extend the Framer's capabilities with plugins for specialized tasks or integrations.
6. **Balance Autonomy and Control**: Allow Framers to make decisions autonomously while providing appropriate constraints and oversight.
7. **Optimize Resource Usage**: Be mindful of API calls and computational resources, especially when working with multiple Framers.
# Framer Component in Framer

The Framer component serves as the central coordinator for all AI agent operations, managing the interplay between various components to create a cohesive and intelligent entity. It processes perceptions, makes decisions, and executes tasks. However, there are scenarios where a decision might not be executed immediately, leading to another decision being made. These scenarios include:

1. **Decision Already Executed**: If a decision has already been executed, the system will skip re-execution to prevent redundant actions. This is typically logged with a message like "Decision already executed, skipping re-execution."

2. **Framer Not Ready**: If the Framer is not in a state to execute decisions (e.g., during initialization or when certain dependencies are not yet loaded), the decision will be queued for later execution.

3. **Invalid Decision**: If the decision is deemed invalid due to missing or incorrect parameters, it may be discarded, prompting the system to make a new decision.

4. **Priority Override**: In some cases, a new perception or context change might lead to a higher-priority decision overriding the current one, causing the system to pivot to the new decision.

These scenarios are crucial for understanding the decision-making process within the Framer component and ensuring that the system operates smoothly and efficiently.
