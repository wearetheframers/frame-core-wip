# Action Registry

## Overview

The `ActionRegistry` class is responsible for managing and executing actions within the Frame framework. It allows for the registration, retrieval, and execution of actions, providing a flexible mechanism for extending the capabilities of Framers.

## Key Features

- **Action Management**: Register, retrieve, and execute actions.
- **Default Actions**: Provides a set of default actions that can be overridden or extended.
- **Priority Handling**: Actions can be prioritized to determine execution order.

## Usage

To use the `ActionRegistry`, initialize it and register actions as needed:

```python
from frame.src.framer.agency.action_registry import ActionRegistry

action_registry = ActionRegistry()

def custom_action():
    print("Performing custom action")

action_registry.register_action(
    action_name="custom_action",
    action_func=custom_action,
    description="A custom action for demonstration purposes",
    priority=5
)

# Execute the action
action_registry.perform_action("custom_action")
```

## API Documentation

::: frame.src.framer.brain.action_registry.ActionRegistry
