---
title: Plugins and Actions
weight: 50
---

# Plugins and Actions

Frame features a powerful and flexible plugin system inspired by game mods, allowing developers to extend the functionality of Framers. This system supports a community marketplace where plugins can be shared, sold, or given away, fostering a rich ecosystem of extensions and customizations. Plugins change Framer behaviors by adding or removing actions.

## Table of Contents

- [[#plugin-naming-and-structure]]
- [[#plugin-system-and-permissions-overview]]
  - [[#permissions-system]]
    - [[#default-permissions]]
    - [[#custom-plugin-permissions]]
    - [[#setting-permissions]]
  - [[#pluginbase-class]]
  - [[#creating-a-new-plugin]]
  - [[#plugin-configuration]]
  - [[#plugin-loading]]
  - [[#using-plugins]]
  - [[#best-practices]]
- [[#actions]]
  - [[#default-actions]]
  - [[#default-plugins]]
  - [[#permissions]]
  - [[#creating-new-actions]]
- [[#example-weather-forecast-plugin]]

## Plugin Naming and Structure

When creating a plugin, it is important to follow a specific naming and directory structure to ensure proper loading and functionality:

1. **Directory Naming**: Each plugin must be stored in its own directory. The directory name should match the plugin name in snake_case format.

2. **Main Plugin File**: Inside the plugin directory, there should be a main plugin file named exactly as the directory, but in snake_case format with a `.py` extension. For example, if your plugin directory is named `audio_transcription_plugin`, the main file should be `audio_transcription_plugin.py`.

3. **Class Naming**: The main class within the plugin file should be named in CamelCase format, derived from the directory name. For example, `AudioTranscriptionPlugin`.

4. **__init__.py File**: Each plugin directory must contain an `__init__.py` file. This file should import the main plugin class to ensure it is accessible when the plugin is loaded. For example:
   ```python
   from .audio_transcription_plugin import AudioTranscriptionPlugin
   ```

5. **Plugin Base Class**: All plugins must inherit from the `BasePlugin` class to ensure they implement the necessary interface for integration with the Frame system.

By adhering to this structure, plugins can be easily discovered and loaded by the Frame system, ensuring a seamless integration process.

When creating a plugin, it is important to follow a specific naming and directory structure to ensure proper loading and functionality:

1. **Directory Naming**: Each plugin must be stored in its own directory. The directory name should match the plugin name in snake_case format.

2. **Main Plugin File**: Inside the plugin directory, there should be a main plugin file named exactly as the directory, but in snake_case format with a `.py` extension. For example, if your plugin directory is named `audio_transcription_plugin`, the main file should be `audio_transcription_plugin.py`.

3. **Class Naming**: The main class within the plugin file should be named in CamelCase format, derived from the directory name. For example, `AudioTranscriptionPlugin`.

4. **__init__.py File**: Each plugin directory must contain an `__init__.py` file. This file should import the main plugin class to ensure it is accessible when the plugin is loaded. For example:
   ```python
   from .audio_transcription_plugin import AudioTranscriptionPlugin
   ```

5. **Plugin Base Class**: All plugins must inherit from the `BasePlugin` class to ensure they implement the necessary interface for integration with the Frame system.

By adhering to this structure, plugins can be easily discovered and loaded by the Frame system, ensuring a seamless integration process.

## Plugin System and Permissions Overview

Frame's plugin system is designed to be flexible and extensible, allowing developers to easily add new functionality to their Framer instances. This overview will cover the key aspects of the plugin system, including the PluginBase class, plugin creation, configuration, loading, usage, and the new permissions system.

### Permissions System

Frame now uses a permissions system to control which plugins and services a Framer has access to. These permissions are specified in the FramerConfig and are mapped to plugins.

#### Default Permissions

There are three default permissions that correspond to core services:

- `withMemory`: Enables access to the Memory service
- `withEQ`: Enables access to the Emotional Intelligence (EQ) service
- `withSharedContext`: Enables access to the Shared Context service

#### Custom Plugin Permissions

For custom plugins, the permission name follows the format `with<PluginName>`. For example:

- `withSearchExtractSummarizePlugin`: Enables access to the Search Extract Summarize plugin

#### Setting Permissions

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

### PluginBase Class

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

### Creating a New Plugin

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

### Plugin Configuration

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

### Plugin Loading

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

### Using Plugins

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

### Best Practices

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

## Actions

Actions in Frame are executable tasks that a Framer can perform. They are concrete implementations of tasks that can be executed in response to decisions made by the Framer. Actions are registered in the Framer's action registry and can be invoked directly by the Framer or automatically in its decision-making as it senses perceptions.

### Default Actions

Frame comes with a set of default actions that are available to all Framers. Actions can potentially lead to the creation of new actions. All default Framer actions can create new actions.

- **AdaptiveDecisionAction**: Makes decisions using an adaptive strategy based on context.
- **CreateNewAgentAction**: Creates new agents within the framework.
- **GenerateRolesAndGoalsAction**: Generates roles and goals for the Framer.
- **ObserveAction**: Processes observations and generates insights or actions.
- **RespondAction**: Generates a default response based on the current context.
- **ThinkAction**: Engages in deep thinking to generate new insights or tasks.
- **ResearchAction**: Conducts research to gather information.
- **ResourceAllocationAction**: Allocates resources based on urgency, risk, and available resources.

### Default Plugins

- **EQService**: Manages emotional intelligence aspects.
- **MemoryService**: Handles memory storage and retrieval.
- **SharedContext**: Manages shared context across components.
- **Mem0SearchExtractSummarizePlugin**: Enables memory retrieval and summarization.

### Permissions

By default, Framers have **no** access to default or installed plugins unless they are specified.

- **with_memory**: Allows access to memory services for storing and retrieving information. While Framer has access to memory by default, if you want it to respond with RAG-like features and automatically determine when to use memory retrieval versus responding without looking into any memories, you need to ensure the `with_mem0_search_extract_summarize` permission is enabled.
- **with_eq**: Enables emotional intelligence features for more nuanced interactions.
- **with_shared_context**: Provides access to shared context services for collaboration.

## Example: Weather Forecast Plugin

### Creating New Actions

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
        # First param is name of action
        # Second param is description of action which is used for contextualizing when the Framer
        # should choose the action
        # Third param is the priority level of the action with 10 being the highest
        super().__init__("my_custom_action", "Description of the action", 3)

    async def execute(self, execution_context: ExecutionContext, **kwargs):
        # Implement action logic here
        return {"result": "Action executed successfully"}
```

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
        return f"Weather for {location}: {weather}, {temperature}C"
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
        return f"Weather for {location}: {weather}, {temperature}C"
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
