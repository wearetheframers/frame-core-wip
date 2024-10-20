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
    SpeedUpVehicleAction,
    ChangeLaneAction,
    StartDrivingAction,
    NoActionAction,
    BrakeVehicleAction,
    AutonomousVehiclePlugin,
)
from frame.src.framer.brain.actions import BaseAction
from frame.src.services.execution_context import ExecutionContext
from frame.src.framer.agency.priority import Priority
from frame.src.framer.brain.decision import Decision
from frame.src.framer.brain.action_registry import ActionRegistry
from frame.src.services.context.execution_context_service import ExecutionContext

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)
logger.addHandler(handler)


class ProcessPerceptionAction(BaseAction):
    def __init__(self, action_registry: ActionRegistry):
        super().__init__(
            "process_perception",
            "Process a perception and make a decision",
            Priority.HIGH,
        )
        self.action_registry = action_registry

    async def execute(self, execution_context: ExecutionContext, **kwargs) -> str:
        perception = kwargs.get("perception")

        if not perception:
            return "Error: Missing perception"

        logger.info(f"\nProcessing perception: {perception}")

        # Analyze the perception and make a decision
        decision = self.analyze_perception(perception)
        logger.info(f"Decision made: {decision}")

        # Execute the decision
        result = await self.execute_decision(execution_context, decision)
        return str(result)

    async def execute_decision(
        self, execution_context: ExecutionContext, decision: Dict[str, Any]
    ) -> str:
        action = decision.get("action")
        if action == "no_action":
            return f"No action taken: {decision.get('reason')}"

        try:
            result = await self.action_registry.execute_action(
                action, execution_context=execution_context, **decision
            )
            return f"Executed {action}: {result}"
        except Exception as e:
            return f"Error executing action {action}: {str(e)}"

    def analyze_perception(self, perception: Dict[str, Any]) -> Dict[str, Any]:
        perception_type = perception.get("type")
        data = perception.get("data", {})

        if perception_type == "visual":
            return self.handle_visual_perception(data)
        elif perception_type == "audio":
            return self.handle_audio_perception(data)
        elif perception_type == "traffic":
            return self.handle_traffic_perception(data)
        else:
            return {
                "action": "no_action",
                "reason": f"Unknown perception type: {perception_type}",
            }

    def handle_visual_perception(self, data: Dict[str, Any]) -> Dict[str, Any]:
        object_type = data.get("object")
        distance = data.get("distance")

        if object_type == "stop sign":
            if distance == "close":
                return {"action": "stop_vehicle", "reason": "Stop sign is close"}
            else:
                return {
                    "action": "slow_down_vehicle",
                    "reason": "Approaching stop sign",
                }
        elif object_type == "pedestrian":
            if distance in ["close", "medium"]:
                return {"action": "slow_down_vehicle", "reason": "Pedestrian detected"}
            else:
                return {"action": "no_action", "reason": "Pedestrian far away"}
        elif object_type == "green light":
            return {"action": "speed_up_vehicle", "reason": "Green light ahead"}
        else:
            return {
                "action": "no_action",
                "reason": f"No specific action for {object_type}",
            }

    def handle_audio_perception(self, data: Dict[str, Any]) -> Dict[str, Any]:
        sound = data.get("sound")
        distance = data.get("distance")

        if sound == "siren":
            if distance == "close":
                return {
                    "action": "change_lane",
                    "reason": "Emergency vehicle approaching",
                }
            else:
                return {
                    "action": "slow_down_vehicle",
                    "reason": "Potential emergency vehicle",
                }
        elif sound == "horn":
            return {"action": "slow_down_vehicle", "reason": "Vehicle honking nearby"}
        else:
            return {"action": "no_action", "reason": f"No specific action for {sound}"}

    def handle_traffic_perception(self, data: Dict[str, Any]) -> Dict[str, Any]:
        condition = data.get("condition")

        if condition == "clear":
            return {"action": "speed_up_vehicle", "reason": "Clear traffic conditions"}
        elif condition == "congested":
            return {"action": "slow_down_vehicle", "reason": "Traffic congestion ahead"}
        elif condition == "accident_ahead":
            return {"action": "change_lane", "reason": "Accident reported ahead"}
        else:
            return {
                "action": "no_action",
                "reason": f"No specific action for {condition}",
            }


async def main():
    frame = Frame()
    config = FramerConfig(name="AutonomousVehicleFramer")
    framer = await frame.framer_factory.create_framer(config, plugins=frame.plugins)

    # Start driving when the script is run
    vehicle_plugin = next(
        (
            plugin
            for plugin in framer.plugins.values()
            if isinstance(plugin, AutonomousVehiclePlugin)
        ),
        None,
    )
    if vehicle_plugin:
        await vehicle_plugin.start_driving()
        logger.info("Vehicle started driving automatically.")
    else:
        logger.warning("AutonomousVehiclePlugin not found. Vehicle not started.")

    action_registry = ActionRegistry()
    action_registry.actions = {}
    action_registry.valid_actions = []

    execution_context = ExecutionContext(llm_service=framer.llm_service)
    execution_context.action_registry = action_registry
    execution_context.agency = framer.agency

    vehicle_plugin = AutonomousVehiclePlugin(framer)
    stop_vehicle_action = StopVehicleAction(vehicle_plugin)
    slow_down_vehicle_action = SlowDownVehicleAction(vehicle_plugin)
    speed_up_vehicle_action = SpeedUpVehicleAction(vehicle_plugin)
    change_lane_action = ChangeLaneAction(vehicle_plugin)
    start_driving_action = StartDrivingAction(vehicle_plugin)
    no_action_action = NoActionAction(vehicle_plugin)
    brake_vehicle_action = BrakeVehicleAction(vehicle_plugin)
    process_perception_action = ProcessPerceptionAction(action_registry)

    action_registry.add_action(stop_vehicle_action)
    action_registry.add_action(slow_down_vehicle_action)
    action_registry.add_action(speed_up_vehicle_action)
    action_registry.add_action(change_lane_action)
    action_registry.add_action(start_driving_action)
    action_registry.add_action(no_action_action)
    action_registry.add_action(brake_vehicle_action)
    action_registry.add_action(process_perception_action)

    framer.brain.action_registry = action_registry
    framer.execution_context = execution_context

    perceptions = [
        {
            "type": "visual",
            "data": {"object": "start", "distance": "close"},
            "source": "camera",
        },
        {
            "type": "visual",
            "data": {"object": "green light", "distance": "medium"},
            "source": "camera",
        },
        {
            "type": "traffic",
            "data": {"condition": "clear"},
            "source": "traffic_system",
        },
        {
            "type": "visual",
            "data": {"object": "pedestrian", "distance": "close"},
            "source": "camera",
        },
        {
            "type": "audio",
            "data": {"sound": "siren", "distance": "far"},
            "source": "microphone",
        },
        {
            "type": "traffic",
            "data": {"condition": "accident_ahead"},
            "source": "traffic_system",
        },
        {
            "type": "visual",
            "data": {"object": "stop sign", "distance": "close"},
            "source": "camera",
        },
    ]

    for perception in perceptions:
        logger.info(f"Processing perception: {perception}")
        result = await action_registry.execute_action(
            "process_perception",
            execution_context=execution_context,
            perception=perception,
        )
        logger.info(f"Action result: {result}")
        await asyncio.sleep(1)

    await framer.close()


if __name__ == "__main__":
    asyncio.run(main())
