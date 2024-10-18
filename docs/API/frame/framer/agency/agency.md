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

- **Role Management**: Assign and manage roles for the [[framer|Framer]]. Roles are active by default, and multiple roles can be active simultaneously.
- **Goal Management**: Set and track goals to guide the [[framer|Framer]]'s actions. Multiple goals can be active at the same time.
- **Task Management**: Create, assign, and complete tasks.
- **Workflow Management**: Organize tasks into workflows to achieve specific objectives.
- **Automatic Role and Goal Generation**: Generate roles and goals when they are not provided or are empty.
- **Action Priority**: Assign priorities to actions to control their execution order and preference.
- **Execution Context**: Utilize a centralized execution context for consistent access to services across actions.

## Usage

To use the Agency class, initialize it with the necessary services and configurations:

```python
from frame.src.framer.agency.agency import Agency
from frame.src.services.llm.main import LLMService
from frame.src.services.context.context_service import Context
from frame.src.framer.agency.execution_context import ExecutionContext

llm_service = LLMService()
context = Context()
execution_context = ExecutionContext(llm_service=llm_service)
agency = Agency(execution_context, context)
```

## Execution Context

The ExecutionContext is a crucial component in the Agency architecture. It serves as a centralized container for various services and state information that actions might need during execution. This approach offers several benefits:

1. **Consistency**: Ensures that all actions have access to the same set of services and state, promoting consistency across the system.
2. **Flexibility**: Makes it easier to add or modify services without changing the signature of every action.
3. **Dependency Injection**: Facilitates better testing and modular design by allowing easy substitution of services.
4. **Reduced Coupling**: Actions no longer need to be directly aware of specific services, reducing dependencies.
5. **State Management**: Provides a centralized location for managing and accessing shared state across actions.

The ExecutionContext includes:

- Language Model Service (LLMService)
- Memory Service (MemoryService)
- Emotional Intelligence Service (EQService)
- Soul component
- Shared state dictionary
- Perception processing function
- Decision execution function
- Framer configuration

By using the ExecutionContext, we can more effectively manage the resources and state available to actions, ensuring they have everything they need to operate within the Framer ecosystem. This design promotes modularity, testability, and flexibility in the Agency's architecture.

## Role and Goal Generation

The Agency class provides methods to automatically generate roles and goals:

- `generate_roles()`: Generates roles based on the Framer's context.
- `generate_goals()`: Generates goals based on the Framer's context.
- `generate_roles_and_goals()`: Generates both roles and goals, or just one of them depending on the current state of the Framer.

The behavior for role and goal generation is as follows:

- If both roles and goals are None, they will be generated using `generate_roles_and_goals()`.
- If roles is an empty list `[]`, no roles or goals will be assigned, as the Agency has no roles to base goals on.
- If goals is an empty list `[]` and roles is None, only goals will be generated.
- If both roles and goals are empty lists `[]`, both will be generated.
- If roles are None or an empty list and goals are provided, roles will be generated and new goals will be added to the existing ones.
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
# Agency

::: frame.src.framer.agency.agency.Agency
    options:
      show_root_heading: false
      show_source: false

## Overview

The `Agency` module represents the decision-making and task management component of a Framer. It manages roles, goals, and tasks, coordinating the Framer's actions and priorities.

## Components

### Roles

Roles define the different functions or personas that the Framer can adopt. Each role has specific responsibilities and expertise areas.

### Goals

Goals represent the objectives that the Framer aims to achieve. They guide the Framer's decision-making process and task prioritization. Goals have different statuses (ACTIVE, COMPLETED, ABANDONED) which influence their impact on the Framer's behavior.

### Tasks

Tasks are specific actions or processes that the Framer needs to complete to achieve its goals. The Agency manages task creation, prioritization, and execution.

## Key Methods

### `generate_roles_and_goals`

Generates initial roles and goals for the Framer based on its configuration and purpose.

### `set_roles`

Sets or updates the Framer's roles.

### `set_goals`

Sets or updates the Framer's goals.

### `get_goals`

Retrieves the current list of goals, including their statuses.

## Usage

The Agency is a core component of the Framer, coordinating its decision-making process:

```python
agency = Agency(llm_service=llm_service, execution_context=execution_context)

# Generate initial roles and goals
roles, goals = await agency.generate_roles_and_goals()

# Update goals
agency.set_goals(new_goals)

# Get current goals
current_goals = agency.get_goals()
```

The Agency ensures that the Framer's actions align with its current goals and roles, taking into account the status of each goal when making decisions or prioritizing tasks.
