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


class TradingSimulation:
    def __init__(self):
        # Initialize Frame and Framer for the trading simulation
        self.frame = Frame()
        self.config = FramerConfig(name="TradingFramer", default_model="gpt-4o-mini")
        self.framer = None

    async def setup(self):
        # Create a Framer instance and register the AdaptiveDecisionAction
        self.framer = await self.frame.create_framer(self.config)
        adaptive_action = AdaptiveDecisionAction()
        self.framer.brain.action_registry.add_action(
            action_or_name=adaptive_action.name,
            action_func=adaptive_action.execute,
            description=adaptive_action.description,
            priority=adaptive_action.priority,
        )

    async def simulate(self):
        # Define scenarios with varying factors
        scenarios = [
            {
                "urgency": 8,
                "risk": 2,
                "resources": "limited",
                "stakeholders": ["investor A"],
            },
            {
                "urgency": 3,
                "risk": 1,
                "resources": "abundant",
                "stakeholders": ["investor B", "investor C"],
            },
            {
                "urgency": 5,
                "risk": 5,
                "resources": "moderate",
                "stakeholders": ["investor D"],
                "deadline": "2024-12-31",
            },
            {
                "urgency": 7,
                "risk": 8,
                "resources": "scarce",
                "stakeholders": ["investor E", "investor F"],
                "deadline": "2024-11-15",
                "dependencies": ["project X", "project Y"],
                "external_factors": ["market volatility", "regulatory changes"],
            },
        ]

        # Process each scenario and make a decision
        for scenario in scenarios:
            print(f"\nScenario: {scenario}")
            decision = await self.framer.brain.action_registry.execute_action(
                "adaptive_decision",
                context=scenario,
            )
            print(f"Decision: {decision}")

    async def close(self):
        # Close the Framer instance
        await self.framer.close()


# Run the trading simulation
if __name__ == "__main__":
    simulation = TradingSimulation()
    asyncio.run(simulation.setup())
    asyncio.run(simulation.simulate())
    asyncio.run(simulation.close())
