import asyncio

import os, sys

# Add the project root to the Python path to ensure all modules can be imported correctly
# If we are running the examples from the source code (not installing package from pip)
# then you need to have this line uncommented.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from frame import Frame, FramerConfig
from frame.src.framer.brain.actions.adaptive_decision_action import (
    AdaptiveDecisionAction,
)


class TaskManagementSimulation:
    def __init__(self):
        # Initialize Frame and Framer for the task management simulation
        self.frame = Frame()
        self.config = FramerConfig(name="TaskFramer", default_model="gpt-4o-mini")
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
        # Define task scenarios with varying priority and deadline
        task_scenarios = [
            {"priority": 9, "deadline": "2024-10-25"},  # High priority, near deadline
            {"priority": 3, "deadline": "2024-11-10"},  # Low priority, far deadline
            {
                "priority": 6,
                "deadline": "2024-10-30",
            },  # Moderate priority, moderate deadline
        ]

        # Process each task scenario and make a task management decision
        for scenario in task_scenarios:
            print(f"\nTask Scenario: {scenario}")
            decision = await self.framer.brain.action_registry.execute_action(
                "adaptive_decision", context=scenario
            )
            print(f"Task Management Decision: {decision}")

    async def close(self):
        # Close the Framer instance
        await self.framer.close()


# Run the task management simulation
if __name__ == "__main__":
    simulation = TaskManagementSimulation()
    asyncio.run(simulation.setup())
    asyncio.run(simulation.simulate())
    asyncio.run(simulation.close())
