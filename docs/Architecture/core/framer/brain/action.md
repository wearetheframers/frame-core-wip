---
title: Action
weight: 50
---

# Action Architecture

## Overview

The Action component represents actionable items for Framers to work on. It includes a description of the action to be performed, a priority level, and can create Tasks with specific output types. Actions are implemented as classes that inherit from a base `Action` class, providing a consistent structure and interface for all actions in the Frame framework.

## Key Features

- Base `Action` class for consistent implementation.
- Action description, name, and priority.
- Asynchronous execution method.
- Integration with ExecutionContext for access to services and state.
- Ability to create Tasks with enforced output types.

## Creating a New Action

To create a new action, follow these steps:

1. Create a new file in the `frame/src/framer/agency/actions/` directory.
2. Import the base `Action` class and `ExecutionContext`.
3. Define a new class that inherits from `Action`.
4. Implement the `__init__` method to set the action name and description.
5. Implement the `execute` method with the action's logic.

Here's an example of creating a new action:

```python
from typing import Dict, Any
from frame.src.services.execution_context import ExecutionContext
from frame.src.framer.agency.actions.base_action import Action
from frame.src.models.framer.agency.priority import Priority

class MyNewAction(Action):
    def __init__(self):
        super().__init__("my_new_action", "Description of what this action does", Priority.MEDIUM)

    async def execute(self, execution_context: ExecutionContext, **kwargs) -> Any:
        # Implement the action logic here
        # Use execution_context to access services and state
        
        # Create a task with an expected output type
        task = self.create_task("Perform a specific operation", expected_output_type=Dict[str, Any])
        
        # Perform the task logic
        result = {"key": "value"}  # This should match the expected output type
        
        # You can return the task or the result directly
        return task  # or return result
```

## Task Creation

Actions can create Tasks, which are more specific actionable items that the Framer can work on. Tasks can enforce output types, allowing for more structured and type-safe operations. The `create_task` method in the `Action` class facilitates this:

```python
task = self.create_task("Task description", expected_output_type=Dict[str, Any])
```

This allows for better control over the expected outputs of tasks and can help in maintaining consistency across the framework.

## Permissions

All plugins require explicit permissions to be used. Users must add all permissions for any plugins they want to use. This ensures that Framers only have access to the plugins they are explicitly allowed to use, providing fine-grained control over their capabilities.

## Related Components

- [[decision]]: Represents a decision made by the Brain component of a Framer, which can lead to action execution and task creation.
- [[actionregistry]]: Manages and executes actions within the Frame framework, facilitating action and task management.
- [[execution_context]]: Provides necessary services and state for action execution.
- [[task]]: Represents a specific actionable item created by an Action, potentially with an enforced output type.
