---
title: Plugins and Actions
weight: 50
---

Frame provides a powerful and flexible plugin system that allows you to extend the functionality of Framers by adding new actions. This system is designed to be as expansive and customizable as mods in games, allowing for unlimited plugins and expansions to be developed. This document explains how to create, register, and use plugins and actions in the Frame framework.

## Introduction

Plugins in Frame are essentially new actions that can be added to the `ActionRegistry`. These actions can be used by Framers to perform specific tasks or integrate with external services. By creating plugins, you can extend the capabilities of your AI agents to handle domain-specific tasks or interact with custom APIs.

Frame will feature a plugin marketplace where premium plugins and community plugins can be developed, given away, or sold. This marketplace will foster a rich ecosystem of extensions and customizations, similar to mod communities in popular games.

## Action Component

**Action Model**: Represents an executable action within the framework.
- Properties:
    - `name` (str): The name of the action.
    - `function` (callable): The function that implements the action logic.
    - `description` (str): A brief description of what the action does.
    - `priority` (int): A priority score from 1 (lowest) to 10 (highest).

These models help standardize the structure of actions and decisions throughout the framework.

## Creating a New Action

To create a new action, follow these steps:

1. Create a new Python file in the `frame/src/framer/agency/actions/` directory (e.g., `my_custom_action.py`).
2. Define a function that implements the action logic.
3. The function should accept any necessary parameters and return the result of the action.

### Example 1: Weather Information Action

Let's create an action that fetches weather information for a given location using an external API.

```python
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
```

### Example 2: Sentiment Analysis Action

Now, let's create an action that performs sentiment analysis on a given text using a sentiment analysis library.

```python
from textblob import TextBlob
from typing import Dict, Any

def analyze_sentiment(text: str, **kwargs) -> Dict[str, Any]:
    """
    Perform sentiment analysis on a given text.
    
    Args:
        text (str): The text to analyze
    
    Returns:
        Dict[str, Any]: Sentiment analysis results
    """
    blob = TextBlob(text)
    sentiment = blob.sentiment
    return {
        "polarity": sentiment.polarity,
        "subjectivity": sentiment.subjectivity
    }
```

## Registering a New Action

To register your new action with the ActionRegistry, follow these steps:

1. Import your action function and the ActionRegistry.
2. Use the `register_action` method to add your action to the registry.

### Registering the Weather Information Action

```python
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
```

### Registering the Sentiment Analysis Action

```python
from frame.src.framer.agency.action_registry import ActionRegistry
from frame.src.framer.agency.actions.sentiment_analysis import analyze_sentiment

action_registry = ActionRegistry()
action_registry.register_action(
    "analyze_sentiment",
    analyze_sentiment,
    description="Perform sentiment analysis on a given text",
    priority=5,
    expected_output_format="A dictionary with polarity and subjectivity",
    expected_output_format_strict="Dict[str, Any]"
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
