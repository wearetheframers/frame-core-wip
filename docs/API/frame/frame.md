# Frame

## Overview

Frame is the main interface for creating and managing Framer instances in the Frame cognitive agent framework. It acts as the central hub for initializing and orchestrating the various components of the framework, providing a flexible and powerful platform for building multi-modal cognitive agents with emergent behaviors.

## Related Components

- [[framer]]: Individual AI agents created and managed by Frame.
- [[framed]]: A collection of Framer objects working together to achieve complex tasks.

## Key Features

Frame includes several default plugins and services that are automatically available to Framers. These include:

- **Services**: `memory`, `eq`, and `shared_context` are special plugins called services. They function like plugins but do not require explicit permissions to be accessed. They are always available to Framers, enhancing their capabilities by providing essential functionalities without the need for additional permissions.

- **Default Plugin**: The `Mem0SearchExtractSummarizePlugin` is included as a default plugin. It provides a response mechanism that requires memory retrieval, functioning as a Retrieval-Augmented Generation (RAG) mechanism. Users must explicitly add permissions for this plugin to enable Framers to search, extract, and summarize information effectively. Plugins are lazily loaded, meaning they are not loaded until the necessary permissions are explicitly added.

- Creation and management of Framer and Framed instances
- Extensible architecture with a powerful plugin engine
- Support for a plugin marketplace, allowing for premium and community plugins
- Flexible plugin system inspired by game mods, enabling unlimited expansions and customizations

By default, the plugins directory is located in the same directory as the `frame` package, inside a folder called `./plugins`. This can be changed by specifying a different directory when initializing the Frame instance:

```python
frame = Frame(plugins_dir="/path/to/custom/plugins")
```

### Attributes

- `openai_api_key` (Optional[str]): API key for OpenAI services. Default is None.
- `mistral_api_key` (Optional[str]): API key for Mistral services. Default is None.
- `huggingface_api_key` (Optional[str]): API key for Hugging Face services. Default is None.
- `default_model` (Optional[str]): The default language model to use. Default is gpt-3.5-turbo.
- `llm_service` (Optional[LLMService]): A custom LLMService instance. If not provided, a default one will be created that checks for the API keys in the environment.
- `_dynamic_model_choice` (bool): Determines if the Framer should dynamically choose the best model based on token size. Default is False.

## Usage Example

```python
from frame import Frame
from frame.framer.config import FramerConfig

# Initialize Frame
frame = Frame(openai_api_key="your_api_key_here")

# Create a Framer
config = FramerConfig(
    name="Research Assistant",
    description="An AI assistant specialized in conducting research",
    default_model="gpt-3.5-turbo"
)

framer = await frame.create_framer(
    config=config,
    roles=[
        {"name": "Researcher", "description": "Conducts in-depth research on various topics"}
    ],
    goals=[
        {"description": "Provide accurate and comprehensive information", "priority": 1.0}
    ],
    soul_seed={"personality": "curious and analytical"}
)

# Use the Framer
result = await framer.sense({"hear": "Tell me about the latest advancements in AI"})
print(result)

# Get a completion directly from Frame
completion = await frame.get_completion("Summarize the key features of Frame")
print(completion)

# Create a Framed group
framed_group = frame.create_framed([framer])
```

This example demonstrates how to initialize a Frame instance, create a Framer with specific configuration, roles, goals, and soul seed, use the Framer to process a query, directly get a completion from the Frame, and create a Framed group.

## Additional Features

### Custom Action Registry

In the autonomous vehicle example, we demonstrate how to replace the default action registry with a custom one. This allows for a more flexible and hackable system where you can replace or extend default behaviors. The `process_perception` function takes precedence over the observe action, showing how you can customize the action registry. You can also remove actions from the Framer behavior in plugins programmatically.

### Multi-modal Support

Frame supports multi-modal cognitive agents, allowing for processing of various input types such as text, images, and potentially other modalities. This feature enables the creation of versatile AI agents capable of understanding and responding to diverse forms of information. Note: DSPy does not support streaming mode.

### Memory Management

Frame incorporates complex memory mechanics, including support for global and multi-user memory storage through the Mem0 system. The memory system intelligently determines when to use memory retrieval based on query analysis:

- Personal queries (containing "my", "I", "we")
- Questions about preferences or past conversations
- User-specific information requests

For general knowledge questions, the system uses direct responses without memory retrieval. This advanced memory management allows Framers to maintain context, learn from past interactions, and make more informed decisions while optimizing response generation.

### Plugin System

The framework includes an extensible architecture with a plugin engine, allowing developers to add custom functionality and extend the capabilities of Framers. For more information on creating and using plugins, refer to the [[plugins]].

### CLI and TUI

Frame provides both a Command Line Interface (CLI) and a Text-based User Interface (TUI) with graphical elements, offering flexible ways to interact with and manage Framers.

## API Documentation

::: frame.Frame
