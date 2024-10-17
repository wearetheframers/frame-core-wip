---
title: Brain
publish: true
---

# Brain

## Overview

The Brain class is a critical component of the [[framer|Framer]], responsible for handling decision-making processes. It integrates perceptions, memories, and thoughts to make informed decisions and guide the [[framer|Framer]]'s actions.

## Key Features

- **Perception Integration**: Processes sensory input to inform decision-making.
- **Memory Utilization**: Uses stored memories to enhance decision accuracy.
- **Thought Generation**: Generates thoughts based on perceptions and memories.

## Usage

To use the Brain class, integrate it with the [[framer|Framer]]'s components:

```python
from frame.src.framer.brain.brain import Brain
from frame.src.services.llm.main import LLMService

llm_service = LLMService()
brain = Brain(llm_service)
```

## Extending Brain with New Actions

To extend the Brain's capabilities, you can add new actions to the ActionRegistry. This allows the Brain to perform additional tasks and make more complex decisions.

### Adding New Actions

1. **Create a New Action File**: Place your new action in the `frame/src/framer/agency/actions` directory. This file should define the logic for your action.

2. **Define the Action Function**: Implement the action logic in a function. This function should accept any necessary parameters and return the result of the action.

3. **Register the Action**: Use the `ActionRegistry` to register your action. Provide a name, the function, a description, and a priority level.

4. **Bind Variables to Action Callbacks**: When registering the action, you can bind additional variables to the action function using keyword arguments.

5. **Update VALID_ACTIONS**: Ensure your action is added to the `VALID_ACTIONS` dictionary in `default_actions.py`.

6. **Example**: Check the `examples/` directory for a complete example of extending the bot with new behavior.

## Related Components

- **Execution Control**: The `can_execute` property in the Framer class determines if decisions are executed automatically.

- [[mind]]: Represents the cognitive processes of a [[framer|Framer]].
- [[perception]]: Represents sensory input or information received by a [[framer|Framer]].
- [[decision]]: Represents the decision-making model used by the Brain.
- [[memory]]: Manages the storage and retrieval of information for the Brain.
- [[agency]]: Manages roles, goals, tasks, and workflows for [[framer|Framers]].
- [[soul]]: Represents the core essence and personality of a [[framer|Framer]].

## API Documentation

::: frame.src.framer.brain.Brain
# Brain

::: frame.src.framer.brain.brain.Brain
    options:
      show_root_heading: false
      show_source: false

## Overview

The `Brain` module represents the cognitive processing unit of a Framer. It is responsible for integrating perceptions, memories, and thoughts to make decisions and generate responses.

## Key Components

### Perception Processing

The Brain processes incoming perceptions, interpreting them in the context of the Framer's current goals and their statuses.

### Decision Making

Based on processed perceptions and current goals, the Brain makes decisions that guide the Framer's actions.

### Memory Integration

The Brain integrates short-term and long-term memories to provide context for decision-making.

## Key Methods

### `process_perception`

Processes an incoming perception, taking into account current goals and their statuses.

### `execute_decision`

Executes a decision made by the Brain.

### `update_goals`

Updates the Brain's understanding of current goals and their statuses.

## Usage

The Brain is a core component of the Framer, handling the cognitive processes:

```python
brain = Brain(llm_service=llm_service, roles=roles, goals=goals)

# Process a perception
decision = await brain.process_perception(perception, current_goals)

# Execute a decision
await brain.execute_decision(decision)

# Update goals
brain.update_goals(new_goals)
```

The Brain's decision-making process considers the status of each goal (ACTIVE, COMPLETED, ABANDONED), prioritizing actions that align with active goals and adapting its behavior as goals are completed or abandoned. This ensures that the Framer's cognitive processes remain aligned with its current objectives and priorities.
