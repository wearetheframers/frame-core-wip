---
title: Plugins and Actions
weight: 50
---

Frame provides a powerful plugin system that allows you to extend the functionality of Framers by adding new actions. This document explains how to create, register, and use plugins and actions in the Frame framework.

## Introduction

Plugins in Frame are essentially new actions that can be added to the `ActionRegistry`. These actions can be used by Framers to perform specific tasks or integrate with external services. By creating plugins, you can extend the capabilities of your AI agents to handle domain-specific tasks or interact with custom APIs.

## Action and Decision Models

Frame uses two important models to represent actions and decisions:

1. **Action Model**: Represents an executable action within the framework.
   - Properties:
     - `name` (str): The name of the action.
     - `function` (callable): The function that implements the action logic.
     - `description` (str): A brief description of what the action does.
     - `priority` (int): A priority score from 1 (lowest) to 10 (highest).

2. **Decision Model**: Represents a decision made by a Framer.
   - Properties:
     - `action` (Action): The chosen Action model to be executed.
     - `parameters` (dict): A dictionary of parameters to be passed to the action function.

These models help standardize the structure of actions and decisions throughout the framework.

## Creating a New Action

To create a new action, follow these steps:

1. Create a new Python file in the `frame/src/framer/agency/actions/` directory (e.g., `my_custom_action.py`).
2. Define a function that implements the action logic.
3. The function should accept any necessary parameters and return the result of the action.

Here's a template for a new action:

```python
from typing import Any, Dict

def my_custom_action(param1: str, param2: int, **kwargs) -> Any:
    """
    Perform a custom action.
    
    Args:
        param1 (str): First parameter description.
        param2 (int): Second parameter description.
        **kwargs: Additional keyword arguments.
    
    Returns:
        Any: The result of the action.
    """
    # Your implementation here
    result = f"Action performed with {param1} and {param2}"
    return result
```

## Registering a New Action

To register your new action with the ActionRegistry, follow these steps:

1. Import your action function and the ActionRegistry.
2. Use the `register_action` method to add your action to the registry.

Here's an example of how to register an action:

```python
from frame.src.framer.agency.action_registry import ActionRegistry
from frame.src.framer.agency.actions.my_custom_action import my_custom_action

action_registry = ActionRegistry()
action_registry.register_action(
    "my_custom_action",
    my_custom_action,
    description="Perform a custom action",
    priority=5,
    expected_output_format="A string describing the action result",
    expected_output_format_strict="str"
)
```

The `register_action` method accepts the following parameters:

- `name` (str): The name of the action (used to call it later).
- `function` (callable): The action function itself.
- `description` (str): A brief description of what the action does.
- `priority` (int): A priority score from 1 (lowest) to 10 (highest).
- `expected_output_format` (str): A verbal description of the expected output format.
- `expected_output_format_strict` (str): An exact type of value to be created/generated.

## Binding Variables to Action Callbacks

When registering an action, you can bind additional variables to the action function using keyword arguments. These bound variables will be passed to the action function when it's called.

Here's an example of binding variables:

```python
action_registry.register_action(
    "my_custom_action",
    my_custom_action,
    description="Perform a custom action",
    priority=5,
    expected_output_format="A string describing the action result",
    expected_output_format_strict="str",
    bound_var1="value1",
    bound_var2="value2"
)
```

In this example, `bound_var1` and `bound_var2` will be passed as keyword arguments to `my_custom_action` when it's called.

## Using a Registered Action

Once an action is registered, it can be used in two ways:

1. As part of the Framer's decision-making process:

```python
decision = await framer.brain.make_decision(some_perception)
if decision.action.name == "my_custom_action":
    result = await framer.brain.execute_decision(decision)
    print(f"Result of my custom action: {result}")
```

2. Called directly through the ActionRegistry:

```python
result = framer.brain.action_registry.perform_action("my_custom_action", "param1_value", 42, kwarg1="extra_value")
print(f"Result of my custom action: {result}")
```

## Best Practices

When creating new actions, consider the following best practices:

1. **Documentation**: Provide clear docstrings for your action functions, including parameter descriptions and return value information.
2. **Error Handling**: Implement proper error handling in your action functions to ensure robustness.
3. **Type Hinting**: Use type hints to make your action's interface clear and to enable better IDE support.
4. **Testability**: Design your actions to be easily testable, possibly by accepting dependencies as parameters.
5. **Configurability**: Where appropriate, make your actions configurable to increase their flexibility and reusability.

## Example: Weather Action

Here's a complete example of creating and using a weather action:

```python
# In frame/src/framer/agency/actions/weather_action.py
import requests
from typing import Dict, Any

def get_weather(location: str, api_key: str, **kwargs) -> Dict[str, Any]:
    """
    Fetch weather information for a given location.
    
    Args:
        location (str): The city and country code, e.g., "London,UK"
        api_key (str): The API key for the weather service
        **kwargs: Additional keyword arguments
    
    Returns:
        Dict[str, Any]: Weather information
    """
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

# In your main application file
from frame.src.framer.agency.action_registry import ActionRegistry
from frame.src.framer.agency.actions.weather_action import get_weather

action_registry = ActionRegistry()
action_registry.register_action(
    "get_weather",
    get_weather,
    description="Fetch weather information for a location",
    priority=5,
    expected_output_format="A dictionary containing weather data",
    expected_output_format_strict="Dict[str, Any]",
    api_key="your_api_key_here"  # Binding the API key to the action
)

# Using the action
weather_data = action_registry.perform_action("get_weather", "London,UK")
print(f"Weather in London: {weather_data['main']['temp']}°C")
```

This example demonstrates how to create a new action, register it with bound variables (the API key), and use it within your application.

By following these guidelines and examples, you can create powerful and flexible actions to extend the capabilities of your Frame-based AI agents.
