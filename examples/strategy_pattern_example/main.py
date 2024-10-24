import asyncio
import os, sys

# Add the project root to the Python path to ensure all modules can be imported correctly
# If we are running the examples from the source code (not installing package from pip)
# then you need to have this line uncommented.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from frame import Frame, FramerConfig
from frame.src.framer.brain.actions.adaptive_decision import (
    AdaptiveDecisionAction,
)


async def main():
    # Initialize Frame
    frame = Frame()

    # Create a Framer instance with the AdaptiveDecisionAction
    config = FramerConfig(name="StrategyFramer", default_model="gpt-4o-mini")
    framer = await frame.create_framer(config)

    # Register the AdaptiveDecisionAction
    adaptive_action = AdaptiveDecisionAction()
    framer.brain.action_registry.add_action(
        action_or_name=adaptive_action.name,
        action_func=adaptive_action.execute,
        description=adaptive_action.description,
        priority=adaptive_action.priority,
    )

    # Define a variety of contexts with increasing complexity
    contexts = [
        # Simple contexts
        {"urgency": 8, "risk": 2},  # Should choose aggressive strategy
        {"urgency": 3, "risk": 1},  # Should choose conservative strategy
        {"urgency": 5, "risk": 5},  # Should choose balanced strategy
        # Real-life scenarios
        {"urgency": 9, "risk": 7, "resources": "limited", "stakeholders": ["team A"]},
        {
            "urgency": 2,
            "risk": 3,
            "resources": "abundant",
            "stakeholders": ["team B", "team C"],
        },
        {
            "urgency": 6,
            "risk": 4,
            "resources": "moderate",
            "stakeholders": ["team D"],
            "deadline": "2024-12-31",
        },
        # Complex layered scenarios
        {
            "urgency": 7,
            "risk": 8,
            "resources": "scarce",
            "stakeholders": ["team E", "team F"],
            "deadline": "2024-11-15",
            "dependencies": ["project X", "project Y"],
            "external_factors": ["market volatility", "regulatory changes"],
        },
        {
            "urgency": 4,
            "risk": 6,
            "resources": "high",
            "stakeholders": ["team G"],
            "deadline": "2025-01-20",
            "dependencies": ["project Z"],
            "external_factors": ["technological advancements", "competitor actions"],
        },
    ]

    # Process each context and make a decision
    for context in contexts:
        print(f"\nContext: {context}")
        decision = await adaptive_action.execute(
            framer.execution_context, context=context
        )
        print(f"Decision: {decision}")

    await framer.close()


if __name__ == "__main__":
    asyncio.run(main())
