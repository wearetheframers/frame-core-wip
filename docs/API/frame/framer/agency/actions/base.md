# Base Action

The Base Action module provides the foundation for all actions in the Frame system. It defines the structure and common functionality that all specific actions should implement.

## BaseAction

::: frame.src.framer.agency.actions.base.BaseAction
    options:
      show_root_heading: false
      show_source: false

The `BaseAction` class is an abstract base class that defines the interface for all actions in the Frame system. It includes methods for executing the action and creating tasks.

### Key Methods

- `execute`: This abstract method must be implemented by all subclasses. It defines the main logic of the action.
- `create_task`: A method to create a new Task with the given description and expected output type.

## Creating Custom Actions

To create a custom action, you should:

1. Import the `BaseAction` class from `frame.src.framer.agency.actions.base`.
2. Create a new class that inherits from `BaseAction`.
3. Implement the `execute` method with your action's logic.

Example:

```python
from frame.src.framer.agency.actions.base import BaseAction
from frame.src.services.execution_context import ExecutionContext

class MyCustomAction(BaseAction):
    async def execute(self, execution_context: ExecutionContext, **kwargs):
        # Implement your action logic here
        pass
```

By following this structure, your custom action will be compatible with the Frame system and can be easily integrated into workflows and decision-making processes.
