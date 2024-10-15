---
title: Plugins
weight: 50
---

Frame provides a powerful plugin system that allows you to extend the functionality of Framers by adding new actions. This document explains how to create, register, and use plugins in the Frame framework.

## Action Files

Each action is implemented in a separate file within the `actions` directory. These files contain the logic for each action and can be extended or modified as needed.

- `create_new_agent.py`: Handles creating a new agent with specific capabilities.
- `generate_roles_and_goals.py`: Generates roles and goals for an agent.
- `research.py`: Performs research on a given topic and summarizes findings.
- `respond.py`: Generates a response to a given input or query.
- `think.py`: Processes information and generates new thoughts or ideas.

## Introduction

Plugins in Frame are essentially new actions that can be added to the `ActionRegistry`. These actions can be used by Framers to perform specific tasks or integrate with external services. By creating plugins, you can extend the capabilities of your AI agents to handle domain-specific tasks or interact with custom APIs.

## Creating a Plugin

To create a plugin, follow these steps:

1. Create a new Python file for your plugin (e.g., `my_plugin.py`). You can also keep multiple actions in one file or add to existing files as needed.
2. Define a function that implements the desired action.
3. (Optional) Create a class that encapsulates related actions and any necessary state.

Here's a basic template for a plugin:

```python
from typing import Any, Dict

def my_custom_action(*args, **kwargs) -> Any:
    """
    Implement your custom action here.
    
    Args:
        *args: Positional arguments passed to the action.
        **kwargs: Keyword arguments passed to the action.
    
    Returns:
        Any: The result of the action.
    """
    # Your implementation here
    return "Result of my custom action"

class MyPlugin:
    def __init__(self):
        # Initialize any necessary state or resources
        pass

    def another_custom_action(self, *args, **kwargs) -> Any:
        """
        Another custom action implemented as a method.
        """
        # Your implementation here
        return "Result of another custom action"
```

## Registering a Plugin and Adding a New Action

To add a new action, follow these steps:

1. Define your action function with the desired logic.
2. Register the action using the `register_action` method, providing a description and priority.
3. Add the action name to the `VALID_ACTIONS` set in `brain.py` to ensure it is recognized as a valid action.

Example:

```python
# Define the action function
def my_new_action(*args, **kwargs):
    # Action logic here
    return "Result of my new action"

# Register the action
framer.brain.action_registry.register_action(
    "my_new_action",
    my_new_action,
    description="Perform my new custom action",
    priority=8,
    expected_output_format="Expected result type of my new action",
    expected_output_format_strict="Exact type of value to be generated"
)

# Add to VALID_ACTIONS in brain.py
Brain.VALID_ACTIONS.add("my_new_action")
```

To register your plugin with a Framer, you need to add your custom actions to the Framer's `ActionRegistry`. You can do this when creating a Framer or at any point during its lifecycle.

Here's how to register a plugin:

```python
from frame import Frame
from frame.src.framer.config import FramerConfig
from frame.src.framer.framer_factory import FramerFactory
from frame.src.services.llm.main import LLMService
from my_plugin import my_custom_action, MyPlugin

async def main():
    frame = Frame()
    llm_service = LLMService()
    config = FramerConfig(name="MyFramer")
    framer_factory = FramerFactory(config, llm_service)
    framer = await framer_factory.create_framer()

    # Register a standalone function with description and priority
    framer.brain.action_registry.register_action(
        "my_custom_action",
        my_custom_action,
        description="Perform a custom action",
        priority=7,
        expected_output_format="Expected result of my custom action",
        expected_output_format_strict="Exact type of value to be generated"
    )

    # Register a method from a class with description and priority
    my_plugin = MyPlugin()
    framer.brain.action_registry.register_action(
        "another_custom_action",
        my_plugin.another_custom_action,
        description="Perform another custom action",
        priority=6,
        expected_output_format="Expected result of another custom action",
        expected_output_format_strict="Exact type of value to be generated"
    )

    # Now your custom actions are available to the Framer

## Adding a New Action

To add a new action, follow these steps:

1. Define your action function with the desired logic.
2. Register the action using the `register_action` method, providing a description and priority.
3. Add the action name to the `VALID_ACTIONS` set in `brain.py` to ensure it is recognized as a valid action.

Example:

```python
# Define the action function
def my_new_action(*args, **kwargs):
    # Action logic here
    return "Result of my new action"

# Register the action
framer.brain.action_registry.register_action(
    "my_new_action",
    my_new_action,
    description="Perform my new custom action",
    priority=8
)

# Add to VALID_ACTIONS in brain.py
Brain.VALID_ACTIONS.add("my_new_action")
```
```

The `register_action` method now accepts optional `description` and `priority` parameters:

- `description` (str): A brief description of what the action does.
- `priority` (int): A priority score from 1 (lowest) to 10 (highest) that affects how the decision-making process chooses which action to perform.
- `expected_output_format` (str): A verbal description of the expected output format.
- `expected_output_format_strict` (str): An exact type of value to be created/generated.

## Using a Plugin

Once a plugin is registered, you can use it like any other action in your Framer. The action will be available in the Framer's decision-making process and can be called programmatically. The Framer will also choose to utilize the plugin and use its action if it makes sense to if it is `acting` (if `act()` has been called).

Here's an example of how to use a registered plugin action:

```python
# Using the plugin action in a decision
decision = await framer.brain.make_decision(some_perception)
if decision.action == "my_custom_action":
    result = await framer.brain.execute_decision(decision)
    print(f"Result of my custom action: {result}")

# Calling the plugin action directly
result = framer.brain.action_registry.perform_action("another_custom_action", arg1, arg2, kwarg1=value1)
print(f"Result of another custom action: {result}")
```

## Best Practices

When creating plugins for Frame, consider the following best practices:

1. **Documentation**: Provide clear documentation for your plugin, including its purpose, required dependencies, and usage examples.
2. **Error Handling**: Implement proper error handling in your plugin actions to ensure robustness and provide meaningful error messages.
3. **Type Hinting**: Use type hints to make your plugin's interface clear and to enable better IDE support.
4. **Configurability**: Make your plugin configurable where appropriate, allowing users to customize its behavior.
5. **Testing**: Write unit tests for your plugin to ensure its functionality and make it easier to maintain.
6. **Versioning**: Use semantic versioning for your plugin and clearly communicate any breaking changes.

## Example: Weather Plugin

For a complete example of how to create and use a weather plugin, check out the `examples/weather_plugin` directory in the Frame project. This example demonstrates:

1. How to create a `WeatherPlugin` class that fetches weather information for a given location.
2. How to register the plugin with a Framer.
3. How to use the plugin both directly and as part of the Framer's decision-making process.

To run the example:

1. Navigate to the `examples/weather_plugin` directory.
2. Replace `"your_api_key_here"` in `main.py` with your actual OpenWeatherMap API key.
3. Run the script using `python main.py`.

This example shows how you can significantly extend the capabilities of your Framers and create more sophisticated AI agents tailored to your specific needs.
