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


class BiddingSimulation:
    def __init__(self):
        # Initialize Frame and Framer for the bidding simulation
        self.frame = Frame()
        self.config = FramerConfig(name="BiddingFramer", default_model="gpt-4o-mini")
        self.framer = None

    async def setup(self):
        # Create a Framer instance and register the AdaptiveDecisionAction
        self.framer = await self.frame.create_framer(self.config)
        adaptive_action = AdaptiveDecisionAction()
        self.framer.brain.action_registry.add_action(
            adaptive_action.name,
            adaptive_action.execute,
            adaptive_action.description,
            adaptive_action.priority,
        )

    async def simulate(self):
        # Define bidding scenarios with varying current bid and time remaining
        bidding_scenarios = [
            {"current_bid": 100, "time_remaining": 5},  # High bid, short time
            {"current_bid": 50, "time_remaining": 30},  # Low bid, ample time
            {"current_bid": 75, "time_remaining": 15},  # Moderate bid, moderate time
        ]

        # Process each bidding scenario and make a bidding decision
        for scenario in bidding_scenarios:
            print(f"\nBidding Scenario: {scenario}")
            decision = await self.framer.brain.action_registry.execute_action(
                "adaptive_decision", context=scenario
            )
            print(f"Bidding Decision: {decision}")

    async def close(self):
        # Close the Framer instance
        await self.framer.close()


# Run the bidding simulation
if __name__ == "__main__":
    simulation = BiddingSimulation()
    asyncio.run(simulation.setup())
    asyncio.run(simulation.simulate())
    asyncio.run(simulation.close())
