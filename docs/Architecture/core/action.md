# Action

## Overview

Actions are fundamental components within the Frame framework, representing tasks or operations that can be performed by Framers. Each action is associated with a function and can have a description, priority, and expected output format.

### Actions vs. Strategies

#### Actions
- **Definition**: Actions are executable tasks that a Framer can perform. They are concrete implementations of tasks that can be executed in response to decisions made by the Framer.
- **Usage**: Actions are registered in the Framer's action registry and can be invoked directly by the Framer or through plugins. They are designed to perform specific operations, such as interacting with external systems, processing data, or executing workflows.
- **Integration**: Actions are integrated into the Framer through plugins or directly within the Framer's core logic. They are prioritized and selected based on the current context, roles, goals, and perceptions.

#### Strategies
- **Definition**: Strategies are decision-making algorithms that determine how a Framer should act in a given situation. They encapsulate different approaches to decision-making, allowing the Framer to adapt its behavior based on the context.
- **Usage**: Strategies are used by the Framer to decide which actions to take. They provide a flexible mechanism for implementing different decision-making paradigms, such as conservative, aggressive, or balanced approaches.
- **Integration**: Strategies are typically implemented as part of the Framer's brain component. They can be dynamically selected and applied based on the current state and context, enabling the Framer to adapt its decision-making process.

### How Framers Use Actions and Strategies

- **Decision-Making Process**: The Framer uses strategies to evaluate the current context and determine the best course of action. This involves selecting an appropriate strategy based on factors such as urgency, risk, and available resources.
- **Action Execution**: Once a decision is made, the Framer executes the corresponding action. This involves invoking the action's logic, which may include interacting with external systems, processing data, or updating the Framer's state.
- **Plugin Interaction**: Plugins can define new actions and strategies, extending the Framer's capabilities. They can register actions with the Framer's action registry and provide custom strategies for decision-making.
- **Framer**: Represents an individual AI agent with capabilities for task management, decision-making, and interaction with language models. Each Framer operates independently but can collaborate with others.
- **Framed**: A collection of Framer objects working together to achieve complex tasks.

## Key Features

- **Functionality**: Actions are linked to specific functions that define their behavior.
- **Description and Priority**: Each action can have a description and prioriaction_ty level, influencing its execution order.
- **Output Format**: Actions can specify expected output formats to ensure consistency.

## Usage

Actions in Frame are executable tasks that a Framer can perform. They are concrete implementations of tasks that can be executed in response to decisions made by the Framer. Actions are registered in the Framer's action registry and can be invoked directly by the Framer or automatically in its decision-making as it senses perceptions.

### Default Actions

Frame comes with a set of default actions that are available to all Framers. Actions can potentially lead to the creation of new actions. All default Framer actions can create new actions.

- **AdaptiveDecisionAction**: Makes decisions using an adaptive strategy based on context.
- **CreateNewAgentAction**: Creates new agents within the framework.
- **GenerateRolesAndGoalsAction**: Generates roles and goals for the Framer.
- **ObserveAction**: Processes observations and generates insights or actions.
- **RespondAction**: Generates a default response based on the current context.
- **ThinkAction**: Engages in deep thinking to generate new insights or tasks.
- **ResearchAction**: Conducts research to gather information.
- **ResourceAllocationAction**: Allocates resources based on urgency, risk, and available resources.

### Creating New Actions

To create a new action, follow these steps:

1. Define a new class that inherits from `BaseAction`.
2. Implement the `execute` method with the action's logic.
3. Register the action with the Framer's action registry.

Example:

```python
from frame.src.framer.brain.actions.base import BaseAction
from frame.src.services import ExecutionContext

class MyCustomAction(BaseAction):
    def __init__(self):
        # First param is name of action
        # Second param is description of action which is used for contextualizing when the Framer
        # should choose the action
        # Third param is the priority level of the action with 10 being the highest
        super().__init__("my_custom_action", "Description of the action", 3)

    async def execute(self, execution_context: ExecutionContext, **kwargs):
        # Implement action logic here
        return {"result": "Action executed successfully"}
```

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

::: frame.src.framer.brain.action_registry.ActionRegistry
