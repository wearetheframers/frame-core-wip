# Action

## Overview

Actions are fundamental components within the Frame framework, representing tasks or operations that can be performed by Framers. Each action is associated with a function and can have a description, priority, and expected output format.

## Key Features

- **Functionality**: Actions are linked to specific functions that define their behavior.
- **Description and Priority**: Each action can have a description and priority level, influencing its execution order.
- **Output Format**: Actions can specify expected output formats to ensure consistency.

## Usage

Actions are typically registered and managed through the `ActionRegistry` in `default_actions.py`. Here's an example of defining and registering an action:

```python
def example_action():
    print("Executing example action")

action_registry.register_action(
    action_name="example_action",
    action_func=example_action,
    description="An example action",
    priority=5
)
```

## API Documentation

::: frame.src.framer.agency.action_registry.ActionRegistry
