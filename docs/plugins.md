---
title: Plugins and Actions
weight: 50
---

Frame provides a powerful and flexible plugin system that allows you to extend the functionality of Framers by adding new actions. This system is designed to be as expansive and customizable as mods in games, allowing for unlimited plugins and expansions to be developed. This document explains how to create, register, and use plugins and actions in the Frame framework.

## Introduction

Plugins in Frame are essentially new actions that can be added to the `ActionRegistry`. These actions can be used by Framers to perform specific tasks or integrate with external services. By creating plugins, you can extend the capabilities of your AI agents to handle domain-specific tasks or interact with custom APIs.

Framers use plugins to enhance their ability to process various types of perceptions (such as text, images, or sounds) and perform a wide range of actions. When a plugin action is well-described, the Framer can make reasonable decisions to take that action based on the current context, its internal thinking process, and the action's priority compared to other possible actions.

The plugin system works in conjunction with the Framer's permission system, which determines which plugins a Framer has access to. This allows for fine-grained control over a Framer's capabilities and ensures that Framers only use actions they are explicitly allowed to perform.

Frame features a plugin marketplace where premium plugins and community plugins can be developed, given away, or sold. This marketplace fosters a rich ecosystem of extensions and customizations, similar to mod communities in popular games.

## Default Plugins and Services

Frame includes several default plugins and services that are automatically available to Framers. These services, such as `LLMService`, `EQService`, `MemoryService`, and `SharedContext`, function as plugins with swappable adapters. This means the underlying implementation of the service can be changed while maintaining the same high-level interface. For instance, instead of using `Mem0`, a `LlamaIndex` adapter could be used. While `LLMService` is passed to the Framer by default, you must specify permissions like `with-eq`, `with-memory`, or `with-shared-context` in the `FramerConfig` to access these services. However, all Framers inherently have permission to access these services without needing explicit permission settings.

- **Services**: `memory`, `eq`, and `shared_context` are special plugins called services. They function like plugins but do not require explicit permissions to be accessed. They are always available to Framers, enhancing their capabilities by providing essential functionalities without the need for additional permissions.

- **Default Plugin**: The `Mem0SearchExtractSummarizePlugin` is included as a default plugin. It provides a mechanism to look into memories, retrieve relevant information, and share insights, functioning as a Retrieval-Augmented Generation (RAG) mechanism. By default, all Framers inherit this action, enabling them to search, extract, and summarize information effectively.

To add a plugin as a default, simply include its permission in the FramerConfig. This ensures that the plugin is automatically available to all Framers without needing to specify it each time. Plugins are loaded automatically during Framer creation.

## Emotional Intelligence in Plugins

Plugins can also leverage the Framer's emotional state to modify their behavior. If the `with_eq` permission is granted, plugins can access the Framer's emotional state and adjust their actions accordingly. This allows for more dynamic and context-aware plugin behavior, enhancing the Framer's ability to respond to complex scenarios.

Plugins are controlled by a permission system. Each plugin has a corresponding permission that must be granted to a Framer for it to use that plugin. Permissions are specified in the FramerConfig when creating a Framer.

The permission format for plugins is `with-<plugin-name>`. For example:
- `with-search-extract-summarize-plugin`: Enables access to the Search Extract Summarize plugin

To give a Framer access to a plugin, include its permission in the FramerConfig:

```python
config = FramerConfig(
    name="Example Framer",
    permissions=["with-memory", "with-eq", "with-search-extract-summarize-plugin"]
)
framer = await frame.create_framer(config)
```

This configuration gives the Framer access to the Memory service, EQ service, and the Search Extract Summarize plugin.

## Base Plugin

All plugins in Frame should inherit from the `BasePlugin` class. This base class provides a common interface and some utility methods for all plugins. Here's an overview of the `BasePlugin` class:

```python
from abc import ABC, abstractmethod
from typing import Any, Dict

class BasePlugin(ABC):
    def __init__(self, framer):
        self.framer = framer

    @abstractmethod
    async def on_load(self):
        pass

    def register_action(self, name: str, func: callable, description: str):
        self.framer.brain.action_registry.register_action(name, func, description)

    def remove_action(self, name: str):
        """
        Remove an action from the action registry by its name.

        Args:
            name (str): The name of the action to remove.
        """
        if name in self.framer.brain.action_registry.actions:
            del self.framer.brain.action_registry.actions[name]
            self.framer.logger.info(f"Action '{name}' removed from registry.")
        else:
            self.framer.logger.warning(f"Action '{name}' not found in registry.")

    @abstractmethod
    async def execute(self, action: str, params: Dict[str, Any]) -> Any:
        pass
```

## Creating a New Plugin

To create a new plugin, follow these steps:

1. Create a new Python file in the `frame/src/plugins/` directory (e.g., `my_custom_plugin.py`).
2. Define a new class that inherits from `PluginBase`.
3. Implement the required methods: `on_load()` and `execute()`.
4. Add any additional methods or attributes specific to your plugin.

Here's an example of a simple custom plugin:

```python
from frame.src.framer.brain.plugin_base import PluginBase
from typing import Any, Dict

class MyCustomPlugin(PluginBase):
    async def on_load(self):
        self.register_action("custom_action", self.custom_action, "Perform a custom action")

    async def execute(self, action: str, params: Dict[str, Any]) -> Any:
        if action == "custom_action":
            return await self.custom_action(params)
        else:
            raise ValueError(f"Unknown action: {action}")

    async def custom_action(self, params: Dict[str, Any]) -> str:
        return f"Custom action executed with params: {params}"
```

## Registering and Using a Plugin

To use a plugin with a Framer instance:

1. Import the plugin
2. Initialize the plugin with the Framer instance
3. Register the plugin with the Framer

Here's an example:

```python
from frame import Frame
from frame.src.framer.config import FramerConfig
from frame.src.plugins.my_custom_plugin import MyCustomPlugin

# Initialize Frame
frame = Frame()

# Create a Framer instance
config = FramerConfig(name="CustomFramer", default_model="gpt-3.5-turbo")
framer = await frame.create_framer(config)

# Initialize and register the plugin
custom_plugin = MyCustomPlugin(framer)
framer.register_plugin("my_custom_plugin", custom_plugin)

# Use the plugin
result = await framer.use_plugin("my_custom_plugin", "custom_action", {"param1": "value1"})
print(result)
```

## Plugin Loading

### Ignoring Folders

The plugin loader is designed to ignore any folders that start with an underscore (`_`). This allows you to keep certain directories in the plugins folder without them being loaded as plugins. This can be useful for storing shared resources, documentation, or other non-plugin files.

### Ignoring Folders

The plugin loader is designed to ignore any folders that start with an underscore (`_`). This allows you to keep certain directories in the plugins folder without them being loaded as plugins. This can be useful for storing shared resources, documentation, or other non-plugin files.

Plugins are loaded automatically by the Frame system. The `load_plugins` function in `frame/src/utils/plugin_loader.py` is responsible for discovering and loading plugins. Here's an overview of how it works:

1. The function scans the specified plugins directory (default is `frame/src/plugins/`).
2. For each subdirectory, it attempts to import a module and find a plugin class.
3. If a valid plugin class is found (inheriting from `PluginBase`), it's instantiated and added to the plugins dictionary.
4. The function checks for conflicting action names across all plugins.
5. If conflicts are found, warnings are logged, and only the first occurrence of an action name is kept.
6. The function also loads plugin-specific configurations from environment variables or a `config.json` file in the plugin's directory.

You can customize the plugins directory by setting the `plugins_dir` parameter when initializing the Frame instance:

```python
frame = Frame(plugins_dir="/path/to/custom/plugins")
```

### Handling Conflicting Actions

When loading plugins, Frame checks for conflicting action names across all plugins. If a conflict is detected:

1. A warning message is logged for each conflicting action.
2. Only the first occurrence of an action name is kept and made available for use.
3. Subsequent actions with the same name are skipped.

This behavior ensures that the system remains stable while still allowing for a wide range of plugins to be loaded. Developers should be aware of this behavior and design their plugins accordingly, using unique action names when possible.

#### Best Practices for Plugin Developers

To avoid conflicts and ensure your plugin's actions are loaded successfully:

1. Use unique and descriptive names for your actions.
2. Prefix action names with your plugin name (e.g., `weather_get_forecast` instead of just `get_forecast`).
3. Document all action names provided by your plugin clearly in its documentation.
4. If your plugin is designed to override or replace actions from another plugin, clearly state this in the documentation and consider providing a way to disable the conflicting actions.

When loading plugins, Frame checks for conflicting action names across all plugins. If a conflict is detected:

1. A warning message is logged for each conflicting action.
2. Only the first occurrence of an action name is kept and made available for use.
3. Subsequent actions with the same name are skipped.

This behavior ensures that the system remains stable while still allowing for a wide range of plugins to be loaded. Developers should be aware of this behavior and design their plugins accordingly, using unique action names when possible.

## Best Practices

When creating plugins, consider the following best practices:

1. **Modularity**: Keep your plugin focused on a specific set of related functionalities.
2. **Error Handling**: Implement proper error handling in your plugin methods.
3. **Documentation**: Provide clear docstrings for your plugin class and methods.
4. **Configuration**: Use the built-in configuration loading system for any plugin-specific settings.
5. **Testing**: Write unit tests for your plugin to ensure its functionality.

By following these guidelines, you can create powerful and flexible plugins to extend the capabilities of your Frame-based AI agents.

## Action Component

**Action Model**: Represents an executable action within the framework.
- Properties:
    - `name` (str): The name of the action.
    - `function` (callable): The function that implements the action logic.
    - `description` (str): A brief description of what the action does.
    - `priority` (int): A priority score from 1 (lowest) to 10 (highest).

These models help standardize the structure of actions and decisions throughout the framework.

## Creating a New Action

To create a new action within a plugin, follow these steps:

1. Define a method in your plugin class that implements the action logic.
2. Register the action in the `on_load` method of your plugin.

Here's an example:

```python
class WeatherPlugin(PluginBase):
    async def on_load(self):
        self.register_action("get_weather", self.get_weather, "Fetch weather information for a location")

    async def execute(self, action: str, params: Dict[str, Any]) -> Any:
        if action == "get_weather":
            return await self.get_weather(params.get("location"), params.get("api_key"))
        else:
            raise ValueError(f"Unknown action: {action}")

    async def get_weather(self, location: str, api_key: str) -> Dict[str, Any]:
        # Implementation of weather fetching logic
        pass
```

## Registering a New Action

Actions are automatically registered when you call `self.register_action()` in your plugin's `on_load()` method. The `register_action` method accepts the following parameters:

- `name` (str): The name of the action (used to call it later).
- `function` (callable): The action function itself.
- `description` (str): A brief description of what the action does.

## Using a Registered Action

Once a plugin is registered with a Framer, its actions can be used as follows:

```python
result = await framer.use_plugin("weather_plugin", "get_weather", {"location": "London,UK", "api_key": "your_api_key"})
print(f"Weather data: {result}")
```

By following these guidelines and examples, you can create powerful and flexible plugins and actions to extend the capabilities of your Frame-based AI agents.
