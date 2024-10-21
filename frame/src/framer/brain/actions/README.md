# AdaptiveDecisionAction

The `AdaptiveDecisionAction` class is a high-level action in the Frame framework, designed to make decisions using an adaptive strategy based on the current context. This class evaluates the urgency and risk associated with a situation to choose the most appropriate decision-making strategy.

## Overview

The `AdaptiveDecisionAction` class uses three main strategies:
- **ConservativeStrategy**: Chosen when the risk is low, indicating a preference for cautious decision-making.
- **AggressiveStrategy**: Chosen when the urgency is high, indicating a need for quick and decisive action.
- **BalancedStrategy**: Chosen when neither urgency nor risk is extreme, indicating a need for a well-rounded approach.

## Context and Risk

- **Context**: Represents the current state of the environment or situation. It includes various factors such as urgency, risk, resources, stakeholders, deadlines, dependencies, and external factors.
- **Urgency**: A measure of how quickly a decision needs to be made. Higher urgency values indicate a need for faster decision-making.
- **Risk**: A measure of the potential negative consequences of a decision. Higher risk values indicate a need for more cautious decision-making.

## Example Usage

Below is an example of how to use the `AdaptiveDecisionAction` class within a Framer instance. This example demonstrates how different contexts lead to different strategies being chosen.

```python
import asyncio
from frame import Frame, FramerConfig
from frame.src.framer.brain.actions.adaptive_decision_action import AdaptiveDecisionAction

async def main():
    # Initialize Frame
    frame = Frame()

    # Create a Framer instance with the AdaptiveDecisionAction
    config = FramerConfig(name="StrategyFramer", default_model="gpt-4o-mini")
    framer = await frame.create_framer(config)

    # Register the AdaptiveDecisionAction
    adaptive_action = AdaptiveDecisionAction()
    framer.brain.action_registry.add_action(
        adaptive_action.name,
        adaptive_action.execute,
        adaptive_action.description,
        adaptive_action.priority,
    )

    # Define a variety of contexts with increasing complexity
    contexts = [
        # Simple contexts
        {"urgency": 8, "risk": 2},  # Should choose aggressive strategy
        {"urgency": 3, "risk": 1},  # Should choose conservative strategy
        {"urgency": 5, "risk": 5},  # Should choose balanced strategy

        # Real-life scenarios
        {"urgency": 9, "risk": 7, "resources": "limited", "stakeholders": ["team A"]},
        {"urgency": 2, "risk": 3, "resources": "abundant", "stakeholders": ["team B", "team C"]},
        {"urgency": 6, "risk": 4, "resources": "moderate", "stakeholders": ["team D"], "deadline": "2024-12-31"},

        # Complex layered scenarios
        {
            "urgency": 7,
            "risk": 8,
            "resources": "scarce",
            "stakeholders": ["team E", "team F"],
            "deadline": "2024-11-15",
            "dependencies": ["project X", "project Y"],
            "external_factors": ["market volatility", "regulatory changes"]
        },
        {
            "urgency": 4,
            "risk": 6,
            "resources": "high",
            "stakeholders": ["team G"],
            "deadline": "2025-01-20",
            "dependencies": ["project Z"],
            "external_factors": ["technological advancements", "competitor actions"]
        }
    ]

    # Process each context and make a decision
    for context in contexts:
        print(f"\nContext: {context}")
        decision = await adaptive_action.execute(framer.execution_context, context=context)
        print(f"Decision: {decision}")

    await framer.close()

if __name__ == "__main__":
    asyncio.run(main())
```

### Detailed Comments

- **Initialization**: The `Frame` and `Framer` are initialized, and the `AdaptiveDecisionAction` is registered with the Framer's action registry.
- **Context Definition**: Various contexts are defined, ranging from simple to complex, to demonstrate how the `AdaptiveDecisionAction` adapts its strategy.
- **Decision Process**: For each context, the `execute` method of `AdaptiveDecisionAction` is called, which evaluates the context and selects the appropriate strategy.
- **Output**: The chosen strategy and decision are printed for each context, illustrating how the action adapts to different situations.

This README provides a comprehensive understanding of the `AdaptiveDecisionAction` class, its purpose, and how it can be used effectively within the Frame framework.
