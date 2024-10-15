---
title: Decision
category: Core Components
weight: 3
publish: true
---

# Decision

## Overview

The Decision class represents the outcome of the decision-making process in the [[brain|Brain]] component of a [[framer|Framer]]. It encapsulates the chosen action, associated parameters, reasoning, confidence level, and priority of the decision.

## Key Features

- **Action Selection**: Specifies the action to be taken by the [[framer|Framer]].
- **Parameter Storage**: Stores relevant parameters for the chosen action.
- **Reasoning Capture**: Records the reasoning behind the decision.
- **Confidence Measurement**: Indicates the confidence level of the decision.
- **Priority Assignment**: Assigns a priority level to the decision.

## Usage

To create and use a Decision object:

```python
from frame.src.framer.brain.decision.decision import Decision

decision = Decision(
    action="respond",
    parameters={"response": "Hello, how can I assist you?"},
    reasoning="User greeted the system, so a response is appropriate.",
    confidence=0.9,
    priority=5
)

print(f"Action to take: {decision.action}")
print(f"Parameters: {decision.parameters}")
print(f"Reasoning: {decision.reasoning}")
print(f"Confidence: {decision.confidence}")
print(f"Priority: {decision.priority}")
```

## Extending Decision-Making with New Actions

To extend the decision-making capabilities, you can add new actions to the ActionRegistry. This allows the Decision class to incorporate new actions into its decision-making process.

### Adding New Actions

1. **Create a New Action File**: Place your new action in the `frame/src/framer/agency/actions` directory. This file should define the logic for your action. You can also keep multiple actions in one file or add to existing files as needed.

2. **Define the Action Function**: Implement the action logic in a function. This function should accept any necessary parameters and return the result of the action.

3. **Register the Action**: Use the `ActionRegistry` to register your action. Provide a name, the function, a description, and a priority level.

4. **Bind Variables to Action Callbacks**: When registering the action, you can bind additional variables to the action function using keyword arguments.

5. **Update VALID_ACTIONS**: Ensure your action is added to the `VALID_ACTIONS` dictionary in `default_actions.py`.

6. **Example**: Check the `examples/` directory for a complete example of extending the bot with new behavior.

## Related Components

- **Execution Control**: The `can_execute` property in the Framer class determines if decisions are executed automatically.

- [[brain]]: Uses the Decision class to represent the outcome of its decision-making process.
- [[agency]]: May use the Decision to determine which actions to take or tasks to create.
- [[framer]]: Executes actions based on the Decision made by the Brain.

## API Documentation

::: frame.src.framer.brain.decision.Decision
