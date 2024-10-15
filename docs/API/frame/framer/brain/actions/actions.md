# Actions

The `ActionRegistry` class in the Frame framework manages and executes actions within the system. It allows for the registration, retrieval, and execution of actions, providing a flexible way to extend the capabilities of Framers.

## ActionRegistry

The `ActionRegistry` class is responsible for managing actions that can be performed by Framers. It inherits from the `ConfigurableMixin`, allowing it to be configured with various options.

### Adding New Actions

To add a new action, follow these steps:

1. **Create a New Action File**: Place your new action in the `frame/src/framer/agency/actions` directory. This file should define the logic for your action. You can also keep multiple actions in one file or add to existing files as needed.

2. **Define the Action Function**: Implement the action logic in a function. This function should accept any necessary parameters and return the result of the action.

3. **Register the Action**: Use the `ActionRegistry` to register your action. Provide a name, the function, a description, and a priority level.

4. **Bind Variables to Action Callbacks**: When registering the action, you can bind additional variables to the action function using keyword arguments.

5. **Update VALID_ACTIONS**: Ensure your action is added to the `VALID_ACTIONS` dictionary in `default_actions.py`.

6. **Example**: Check the `examples/` directory for a complete example of extending the bot with new behavior.

Here's a quick example of adding a new action:

```python
# In frame/src/framer/agency/actions/my_action.py
def my_custom_action(param1, param2):
    # Action logic here
    return f"Action performed with {param1} and {param2}"

# Registering the action
from frame.src.framer.agency.action_registry import ActionRegistry

action_registry = ActionRegistry()
action_registry.register_action(
    "my_custom_action",
    my_custom_action,
    description="Perform a custom action",
    priority=5
)
```

### Attributes

- `actions` (Dict[str, Callable]): A dictionary mapping action names to their corresponding functions.

### Methods

#### `__init__(*args, **kwargs)`

Initializes the ActionRegistry with a set of default actions.

#### `register_action(action_name: str, action_func: Callable, description: str = "", priority: int = 5, expected_output: str = "")`

Registers a new action or overrides an existing one.

- `action_name` (str): The name of the action to register.
- `action_func` (Callable): The function to be called when the action is performed.
- `description` (str, optional): A brief description of the action. Defaults to an empty string.
- `priority` (int, optional): The priority of the action, from 1 (lowest) to 10 (highest). Defaults to 5.
- `expected_output` (str, optional): The expected format of the output. Defaults to an empty string.

#### `get_valid_actions() -> List[str]`

Returns a list of all registered action names.

#### `perform_action(action_name: str, *args, callback=None, callback_args=None, **kwargs) -> Any`

Performs a registered action.

- `action_name` (str): The name of the action to perform.
- `*args`: Positional arguments to pass to the action function.
- `callback` (Optional[Callable]): A function to call after the action is completed.
- `callback_args` (Optional[Dict]): Arguments to pass to the callback function.
- `**kwargs`: Keyword arguments to pass to the action function.

Returns the result of the action function.

Raises `ValueError` if the action_name is not registered.

If a callback is provided, it will be called with the result of the action and any additional arguments specified in `callback_args`.

### Default Actions

The ActionRegistry comes with a set of default actions:

1. `create_new_agent`: Creates a new agent with specific capabilities.
2. `generate_roles`: Generates roles for an agent based on the current context.
3. `generate_goals`: Generates goals for an agent based on the current context and roles.
4. `generate_tasks`: Generates tasks for an agent to achieve its goals.
5. `research`: Performs research on a given topic and summarizes findings.
6. `respond`: Generates a response to a given input or query.
7. `wait`: Waits for a specified amount of time or until a condition is met.
8. `error`: Handles and reports an error condition.
9. `think`: Simulates thinking or processing information to reach a conclusion.
10. `speak`: Generates speech or text output for communication.
11. `listen`: Processes and interprets audio or text input.
12. `move`: Simulates movement or change in position within an environment.
13. `use`: Uses or interacts with an object or concept in the environment.
14. `observe`: Observes and processes information from the environment.

Each of these default actions includes a description and expected output format. They can be overridden or extended by registering a new action with the same name.

## Action Files

Each action is implemented in a separate file within the `actions` directory. These files contain the logic for each action and can be extended or modified as needed.

- `create_new_agent.py`: Handles creating a new agent with specific capabilities.
- `generate_roles_and_goals.py`: Generates roles and goals for an agent.
- `research.py`: Performs research on a given topic and summarizes findings.
- `respond.py`: Generates a response to a given input or query.
- `think.py`: Processes information and generates new thoughts or ideas.

## Usage

To use the ActionRegistry in your Framer:

```python
from frame.src.framer.brain.actions import ActionRegistry

# Create an ActionRegistry instance
action_registry = ActionRegistry()

# Register a custom action
def custom_action(param1, param2):
    return f"Custom action performed with {param1} and {param2}"

action_registry.register_action("custom_action", custom_action)

# Perform the custom action
result = action_registry.perform_action("custom_action", "value1", "value2")
print(result)  # Output: Custom action performed with value1 and value2

# Get all valid actions
valid_actions = action_registry.get_valid_actions()
print(valid_actions)  # Output: ['create_new_agent', 'generate_roles', ..., 'custom_action']
```

By using the ActionRegistry, you can easily extend the capabilities of your Framers and create custom behaviors tailored to your specific use case.
