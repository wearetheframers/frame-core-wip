# ActionRegistry

::: frame.src.framer.brain.action_registry.ActionRegistry
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

Registers a new action with the specified name, function, description, and priority. It can now accept an `Action` object directly.

### `execute_action`

Executes a registered action by its name, passing any required parameters.

### `get_all_actions`

Retrieves all registered actions as a dictionary.

## Default Actions

The ActionRegistry now includes the following default actions:

- CreateNewAgentAction
- GenerateRolesAndGoalsAction
- ObserveAction
- RespondAction
- ThinkAction

These actions are automatically registered when the ActionRegistry is initialized.

## Usage

To register a new action:

```python
from frame.src.framer.agency.actions import CustomAction

custom_action = CustomAction()
action_registry.register_action(custom_action)
```

To execute an action:

```python
result = await action_registry.execute_action("custom_action", parameters={})
```
