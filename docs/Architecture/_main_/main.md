# Frame Architecture

## Overview

Frame is a multi-modal cognitive agent framework designed to support fully emergent characteristics. It consists of three main components: `Frame`, `Framed`, and `Framer`. Each component plays a crucial role in the overall architecture, enabling the creation and management of AI agents with complex behaviors and interactions.

## Components

### Frame

The `Frame` class serves as the main interface for creating and managing `Framer` instances. It acts as the central hub for initializing and orchestrating the various components of the framework. The `Frame` class is responsible for:

1. **Initializing and managing the language model service**: It sets up the necessary API keys and initializes the language model service, ensuring that all Framers have access to the required language models.

2. **Creating new Framer instances**: The `Frame` class uses the `FramerBuilder` to construct new Framers based on specified configurations. This encapsulates the complexity of Framer creation and ensures proper initialization.

3. **Setting and managing the default language model**: The `Frame` class provides methods to set and retrieve the default language model, ensuring consistency across the entire Frame ecosystem.

4. **Providing a high-level interface for language model completions**: It offers a consistent interface for getting completions from the language model, abstracting the underlying complexity.

### Framer

The `Framer` class represents an individual AI agent with capabilities for task management, decision-making, and interaction with language models. Each Framer operates independently but can collaborate with others. Key features of the `Framer` class include:

- **Task Management**: Framers can perform tasks asynchronously, leveraging the language model service for text generation and decision-making.

- **Decision-Making**: The `Brain` component within a Framer processes perceptions and makes decisions based on current goals and roles.

- **Interaction with Language Models**: Framers use the `LLMService` to interact with language models, generating text completions and processing perceptions.

- **Memory and Emotional Intelligence**: Framers can be equipped with memory and emotional intelligence capabilities, allowing them to learn from past experiences and adapt their behavior.

### Framed

The `Framed` class represents a collection of `Framer` objects working together to achieve complex tasks. It enables coordination and communication between multiple Framers, allowing for scalable and collaborative operations. The `Framed` class provides:

- **Coordination of Multiple Framers**: It manages the interactions between Framers, facilitating task delegation and collaboration.

- **Sequential and Parallel Processing**: Framers within a `Framed` group can process tasks sequentially or in parallel, depending on the specified configuration.

- **Shared Context and Goals**: The `Framed` class allows Framers to share context and goals, enabling them to work towards common objectives.

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

This architecture allows for a flexible, learning-capable AI agent system that can handle complex tasks while maintaining a consistent personality and improving over time.

## Design Considerations

The design of Frame's architecture is driven by several key considerations:

- **Modularity**: The architecture is highly modular, allowing for easy extension and customization. Each component is designed to be independent, enabling developers to add new features or modify existing ones without affecting the entire system.

- **Scalability**: Frame is designed to scale with the needs of the application. The `Framed` class allows for the creation of large groups of Framers, enabling the system to handle complex tasks and interactions.

- **Flexibility**: The architecture supports a wide range of use cases, from simple task management to complex decision-making and collaboration. The use of language models and memory services allows Framers to adapt to different scenarios and requirements.

- **Extensibility**: Frame's plugin system allows developers to add new actions and capabilities to Framers, enabling them to customize the behavior of their AI agents.

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
    ├── Context
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
│   ├── DSPy Adapter
│   ├── HuggingFace Adapter
│   └── LMQL Adapter
├── MemoryService
│   └── Memory Adapters
│       └── Mem0Adapter
├── EQService
└── ContextService
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

## Conclusion

Frame's architecture provides a robust and flexible framework for creating and managing cognitive agents with emergent behaviors. By leveraging the power of language models and modular design, Frame enables the development of AI agents capable of handling complex tasks and interactions, while maintaining a consistent personality and improving over time.

