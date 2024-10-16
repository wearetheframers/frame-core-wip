# ActionRegistry

::: frame.src.framer.agency.action_registry.ActionRegistry
    options:
      show_root_heading: false
      show_source: false

## Overview

The `ActionRegistry` class is responsible for managing actions within the Framer framework. It allows for the registration, execution, and retrieval of actions, providing a flexible mechanism to extend the capabilities of Framers.

### Attributes

- `actions` (Dict[str, Dict[str, Any]]): A dictionary of registered actions.
- `execution_context` (ExecutionContext): The context in which actions are executed.

## Methods

### `register_action`

Registers a new action with the specified name, function, description, and priority.

### `perform_action`

Executes a registered action by its name, passing any required arguments and an optional callback.

### `get_all_actions`

Retrieves all registered actions as a dictionary.

## Usage

To register a new action:

```python
action_registry.register_action(
    "new_action",
    new_action_function,
    "Description of the new action",
    priority=5
)
```

To perform an action:

```python
result = await action_registry.perform_action("new_action", arg1, arg2)
```
