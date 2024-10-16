# Default Actions

## Overview

The `default_actions` module provides a set of predefined actions that can be used within the Framer framework. These actions are registered by default and can be extended or modified as needed.

### Attributes

- `VALID_ACTIONS` (Dict[str, Dict[str, Any]]): A dictionary of valid actions with their corresponding functions, descriptions, and priorities.

## Functions

### `extend_valid_actions`

Extends the `VALID_ACTIONS` dictionary with new actions provided as a dictionary.

## Usage

To extend the default actions:

```python
new_actions = {
    "custom_action": {
        "func": custom_action_function,
        "description": "A custom action",
        "priority": 3
    }
}
extend_valid_actions(new_actions)
```

To access a default action:

```python
action = VALID_ACTIONS.get("respond")
```
