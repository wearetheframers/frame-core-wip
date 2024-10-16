---
title: Framer
weight: 20
---

# Framer Architecture

## Overview

The Framer class represents an individual AI agent within the Frame cognitive agent framework. It serves as the core component, enabling the creation and management of intelligent agents with capabilities for task management, decision-making, and interaction with language models. Framers are designed to exhibit emergent behaviors and can be customized for various applications.

### Attributes

- `config` (FramerConfig): Configuration settings for the Framer.
- `llm_service` (LLMService): The language model service to be used by the Framer.
- `context_service` (Optional[ContextService]): Service for managing context. Default is None.
- `memory_service` (Optional[MemoryService]): Service for managing memory. Default is None.
- `soul_seed` (Optional[Dict[str, Any]]): Initial seed for the Framer's soul. Default is None.
- `_streamed_response` (dict): A dictionary with keys `status` and `result` that accumulates streamed content when `get_completion` is called with streaming enabled. Resets with each new call.

## Related Components

- [[agency]]: Manages roles, goals, tasks, and workflows for Framers.
- [[brain]]: Handles decision-making processes, integrating perceptions, memories, and thoughts.
- [[soul]]: Represents the core essence and personality of a Framer.
- [[mind]]: Represents the cognitive processes of a Framer.

## Initialization and Key Features

### Initialization

To initialize a `Framer` with roles and goals, use the `initialize()` method. This method will automatically call `act()`, enabling the `Framer` to start processing perceptions and making decisions. The `act()` method sets the Framer to an active state, allowing it to respond to perceptions and execute tasks. If you need to stop the `Framer` from acting or making new tasks, use the `halt()` method. The `halt()` method is crucial for pausing the Framer's activities without shutting it down completely.

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
