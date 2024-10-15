---
title: Agency
category: Core Components
weight: 2
publish: true
---

# Agency

## Overview

The Agency class represents the decision-making and task management component of a [[framer|Framer]]. It is responsible for managing roles, goals, tasks, and workflows, ensuring that the [[framer|Framer]] can operate efficiently and effectively.

## Key Features

- **Role Management**: Assign and manage roles for the [[framer|Framer]].
- **Goal Management**: Set and track goals to guide the [[framer|Framer]]'s actions.
- **Task Management**: Create, assign, and complete tasks.
- **Workflow Management**: Organize tasks into workflows to achieve specific objectives.
- **Automatic Role and Goal Generation**: Generate roles and goals when they are not provided or are empty.

## Usage

To use the Agency class, initialize it with the necessary services and configurations:

```python
from frame.src.framer.agency.agency import Agency
from frame.src.services.llm.main import LLMService
from frame.src.services.context.context_service import Context

llm_service = LLMService()
context = Context()
agency = Agency(llm_service, context)
```

## Role and Goal Generation

The Agency class provides methods to automatically generate roles and goals:

- `generate_roles()`: Generates roles based on the Framer's context.
- `generate_goals()`: Generates goals based on the Framer's context.
- `generate_roles_and_goals()`: Generates both roles and goals, or just one of them depending on the current state of the Framer.

The behavior for role and goal generation is as follows:

- If both roles and goals are None, they will be generated using `generate_roles_and_goals()`.
- If roles is an empty list `[]` and goals is None, only roles will be generated.
- If goals is an empty list `[]` and roles is None, only goals will be generated.
- If both roles and goals are empty lists `[]`, both will be generated.
- If either roles or goals is provided (not None or empty list), the provided value will be used.

## Extending Agency with New Actions

To extend the Agency's capabilities, you can add new actions to the ActionRegistry. This allows the Agency to perform additional tasks and manage new workflows.

### Adding New Actions

1. **Create a New Action File**: Place your new action in the `frame/src/framer/agency/actions` directory. This file should define the logic for your action.

2. **Define the Action Function**: Implement the action logic in a function. This function should accept any necessary parameters and return the result of the action.

3. **Register the Action**: Use the `ActionRegistry` to register your action. Provide a name, the function, a description, and a priority level.

4. **Bind Variables to Action Callbacks**: When registering the action, you can bind additional variables to the action function using keyword arguments.

5. **Update VALID_ACTIONS**: Ensure your action is added to the `VALID_ACTIONS` dictionary in `default_actions.py`.

6. **Example**: Check the `examples/` directory for a complete example of extending the bot with new behavior.

## Related Components

- [[task]]: Represents a task within the [[frame|Frame-Core]] system.
- [[workflow]]: Represents a sequence of related tasks to achieve a specific goal.
- [[framer]]: The main AI agent that uses the Agency for task and goal management.
- [[brain]]: Handles decision-making processes, integrating with the Agency for task execution.

## API Documentation

::: frame.src.framer.agency.Agency
