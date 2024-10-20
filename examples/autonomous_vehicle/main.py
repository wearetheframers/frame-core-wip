import sys
import logging
import os
import asyncio
from typing import Dict, Any

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from frame import Frame, FramerConfig
from autonomous_vehicle_plugin import (
    StopVehicleAction,
    SlowDownVehicleAction,
    ChangeLaneAction,
    AutonomousVehiclePlugin,
)
from frame.src.framer.agency.actions import BaseAction
from frame.src.services.execution_context import ExecutionContext
from frame.src.framer.agency.priority import Priority
from frame.src.framer.brain.decision import Decision
from frame.src.framer.agency.action_registry import ActionRegistry

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)
logger.addHandler(handler)


class ProcessPerceptionAction(BaseAction):
    """
    This replaces some default actions in our Framer like observe etc.
    It is just meant as a custom function that allows low-level decision-making control
    suitable for a self-driving vehicle. It demonstrates the logic flow in perception processing
    and decision-making.
    """

    def __init__(self):
        super().__init__(
            "process_perception",
            "Process a perception and make a decision",
            Priority.HIGH,
        )

    async def execute(
        self, execution_context: ExecutionContext, perception: Dict[str, Any]
    ) -> str:
        logger.info(f"\nProcessing perception: {perception}")
        decision = await execution_context.process_perception(perception)
        logger.info(f"Decision made: {decision}")

        if isinstance(decision, Decision):
            await execution_context.execute_decision(decision)
            return str(decision)
        else:
            raise ValueError(f"Expected a Decision object, but got {type(decision)}")


async def main():
    frame = Frame()
    config = FramerConfig(name="AutonomousVehicleFramer")
    framer = await frame.framer_factory.create_framer(config, plugins=frame.plugins)

    # This completely replaces the ActionRegistry and the default actions in the original Framer
    # (By default Framers come with an ActionRegistry created so there's no need to pass one)
    action_registry = ActionRegistry()
    action_registry.actions = {}
    action_registry.valid_actions = []

    # We must set our newly created Action Registry to our Framer's execution_context
    action_registry.execution_context = framer.brain.agency.execution_context
    vehicle_plugin = AutonomousVehiclePlugin(framer)
    stop_vehicle_action = StopVehicleAction(vehicle_plugin)
    slow_down_vehicle_action = SlowDownVehicleAction(vehicle_plugin)
    change_lane_action = ChangeLaneAction(vehicle_plugin)

    action_registry.add_action(stop_vehicle_action)
    action_registry.add_action(slow_down_vehicle_action)
    action_registry.add_action(change_lane_action)

    process_perception_action = ProcessPerceptionAction()
    action_registry.add_action(process_perception_action)

    # Now we set our Framer's existing action_registry to our new action registry
    framer.brain.agency.action_registry = action_registry

    # This behavior is desirable in this case as a self-driving vehicle has no need to do typical Framer responses
    # like research, respond, etc. and it is safer to keep actions to a minimal amount for a self-driving vehicle.

    perceptions = [
        {
            "type": "visual",
            "data": {"object": "stop sign", "distance": "far"},
            "source": "camera",
        },
        {
            "type": "visual",
            "data": {"object": "stop sign", "distance": "close"},
            "source": "camera",
        },
        {
            "type": "visual",
            "data": {"object": "pedestrian", "distance": "medium"},
            "source": "camera",
        },
        {
            "type": "audio",
            "data": {"sound": "siren", "distance": "far"},
            "source": "microphone",
        },
        {
            "type": "audio",
            "data": {"sound": "siren", "distance": "close"},
            "source": "microphone",
        },
    ]

    for perception in perceptions:
        logger.info(f"Processing perception: {perception}")
        # The sense method allows the Framer to choose any type of action from its behavior,
        # though it intelligently chooses the most relevant / urgent action to take
        # decision = await framer.sense(perception)
        # You could instead enforce a specific action like so
        decision = await framer.sense(perception)
        # The process_perception action we've defined results in a new action or decision based on the perception
        logger.info(f"Decision made: {decision}")
        if decision:
            result = await framer.brain.agency.execute_action(
                decision.action, decision.parameters
            )
            logger.info(f"Decision result: {result}")
        else:
            logger.warning("No decision was made.")
        await asyncio.sleep(1)

    await framer.close()


if __name__ == "__main__":
    asyncio.run(main())
