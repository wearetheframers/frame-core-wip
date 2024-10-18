# Plugin System and Permissions Overview

Frame's plugin system is designed to be flexible and extensible, allowing developers to easily add new functionality to their Framer instances. This overview will cover the key aspects of the plugin system, including the PluginBase class, plugin creation, configuration, loading, usage, and the new permissions system.

## Permissions System

Frame now uses a permissions system to control which plugins and services a Framer has access to. These permissions are specified in the FramerConfig and are mapped to plugins.

### Default Permissions

There are three default permissions that correspond to core services:

- `withMemory`: Enables access to the Memory service
- `withEQ`: Enables access to the Emotional Intelligence (EQ) service
- `withSharedContext`: Enables access to the Shared Context service

### Custom Plugin Permissions

For custom plugins, the permission name follows the format `with<PluginName>`. For example:

- `withSearchExtractSummarizePlugin`: Enables access to the Search Extract Summarize plugin

### Setting Permissions

You can set permissions when creating a Framer:

```python
config = FramerConfig(
    name="Example Framer",
    default_model="gpt-4o-mini",
    permissions=["withMemory", "withEQ", "withSearchExtractSummarizePlugin"]
)
framer = await frame.create_framer(config)
```

This configuration gives the Framer access to the Memory service, EQ service, and the Search Extract Summarize plugin.

## PluginBase Class

All plugins in Frame should inherit from the `PluginBase` class. This abstract base class provides a common interface and utility methods for all plugins. Here's an overview of the `PluginBase` class:

```python
from abc import ABC, abstractmethod
from typing import Any, Dict

class PluginBase(ABC):
    def __init__(self, framer):
        self.framer = framer

    @abstractmethod
    async def on_load(self):
        pass

    def register_action(self, name: str, func: callable, description: str):
        self.framer.brain.action_registry.register_action(name, func, description)

    @abstractmethod
    async def execute(self, action: str, params: Dict[str, Any]) -> Any:
        pass
```

The `PluginBase` class provides:
- An `__init__` method that takes a Framer instance.
- An abstract `on_load` method that should be implemented to perform any initialization when the plugin is loaded.
- A `register_action` method to register new actions with the Framer's action registry.
- An abstract `execute` method that should be implemented to handle plugin-specific actions.

## Creating a New Plugin

To create a new plugin:

1. Create a new Python file in the `frame/src/plugins/` directory.
2. Define a class that inherits from `PluginBase`.
3. Implement the required `on_load()` and `execute()` methods.
4. Add any additional methods or attributes specific to your plugin.

Example:

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

## Plugin Configuration

Plugins can be configured using either environment variables or a `config.json` file within each plugin's directory. The system follows this priority order when looking for configuration:

1. Environment variables (highest priority)
2. `.env` file in the project root
3. `config.json` file in the plugin's directory

For example, to set an API key for a plugin:

1. Set an environment variable: `PLUGIN_API_KEY=your_api_key_here`
2. Add it to your `.env` file: `PLUGIN_API_KEY=your_api_key_here`
3. Create a `config.json` file in the plugin's directory:

```json
{
  "PLUGIN_API_KEY": "your_api_key_here"
}
```

## Plugin Loading

Plugins are loaded automatically by the Frame system based on the permissions specified in the FramerConfig. The `load_plugins` function in `frame/src/utils/plugin_loader.py` now respects these permissions:

1. Scans the specified plugins directory (default is `frame/src/plugins/`).
2. Checks the permissions in the FramerConfig.
3. Attempts to import modules and find plugin classes for permitted plugins.
4. Instantiates valid plugin classes (those inheriting from `PluginBase`).
5. Loads plugin-specific configurations from environment variables or `config.json` files.

You can customize the plugins directory when initializing the Frame instance:

```python
frame = Frame(plugins_dir="/path/to/custom/plugins")
```

## Using Plugins

To use a plugin with a Framer instance:

1. Create a Framer instance with the appropriate permissions.
2. The plugin will be automatically loaded if it's in the correct directory and the Framer has the necessary permission.
3. Use the plugin through the Framer's `use_plugin` method.

Example:

```python
from frame import Frame
from frame.src.framer.config import FramerConfig

# Initialize Frame
frame = Frame()

# Create a Framer instance with specific permissions
config = FramerConfig(
    name="CustomFramer",
    default_model="gpt-3.5-turbo",
    permissions=["withMemory", "withMyCustomPlugin"]
)
framer = await frame.create_framer(config)

# Use the plugin (assuming MyCustomPlugin is in the plugins directory and permission is granted)
result = await framer.use_plugin("my_custom_plugin", "custom_action", {"param1": "value1"})
print(result)
```

## Best Practices

When creating and using plugins:

1. Keep plugins focused on specific functionalities.
2. Implement proper error handling in plugin methods.
3. Provide clear documentation for your plugin class and methods.
4. Use the built-in configuration loading system for plugin-specific settings.
5. Write unit tests for your plugins to ensure their functionality.
6. Use meaningful permission names that clearly indicate the plugin's functionality.
7. Only grant necessary permissions to Framers to maintain security and performance.

By following these guidelines, you can create powerful and flexible plugins to extend the capabilities of your Frame-based AI agents while maintaining control over which capabilities are available to each Framer.

For more details on specific plugins and advanced usage, please refer to the other sections in this documentation.
