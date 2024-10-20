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
    """
    This replaces some default actions in our Framer like observe etc.
    It is just meant as a custom function that allows low-level decision-making control
    suitable for a self-driving vehicle. It demonstrates the logic flow in perception processing
    and decision-making.
    """

    def __init__(self, action_registry: ActionRegistry):
        super().__init__(
            "process_perception",
            "Process a perception and make a decision",
            Priority.HIGH,
        )
        self.action_registry = action_registry

    async def execute(self, execution_context: ExecutionContext, **kwargs) -> str:
        perception = kwargs.get('perception')
        
        if not perception:
            return "Error: Missing perception"

        logger.info(f"\nProcessing perception: {perception}")
        
        # Analyze the perception and make a decision
        decision = self.analyze_perception(perception)
        logger.info(f"Decision made: {decision}")

        # Execute the decision
        result = await self.execute_decision(execution_context, decision)
        return str(result)

    async def execute_decision(self, execution_context: ExecutionContext, decision: Dict[str, Any]) -> str:
        action = decision.get('action')
        if action == 'no_action':
            return f"No action taken: {decision.get('reason')}"
        
        try:
            result = await self.action_registry.execute_action(action, execution_context=execution_context, **decision)
            return f"Executed {action}: {result}"
        except Exception as e:
            return f"Error executing action {action}: {str(e)}"

    def analyze_perception(self, perception: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze the perception and return a decision."""
        perception_type = perception.get('type')
        data = perception.get('data', {})

        if perception_type == 'visual':
            return self.handle_visual_perception(data)
        elif perception_type == 'audio':
            return self.handle_audio_perception(data)
        else:
            return {"action": "no_action", "reason": f"Unknown perception type: {perception_type}"}

    def handle_visual_perception(self, data: Dict[str, Any]) -> Dict[str, Any]:
        object_type = data.get('object')
        distance = data.get('distance')

        if object_type == 'stop sign':
            if distance == 'close':
                return {"action": "stop_vehicle", "reason": "Stop sign is close"}
            else:
                return {"action": "slow_down_vehicle", "reason": "Approaching stop sign"}
        elif object_type == 'pedestrian':
            if distance in ['close', 'medium']:
                return {"action": "slow_down_vehicle", "reason": "Pedestrian detected"}
            else:
                return {"action": "no_action", "reason": "Pedestrian far away"}
        else:
            return {"action": "no_action", "reason": f"No specific action for {object_type}"}

    def handle_audio_perception(self, data: Dict[str, Any]) -> Dict[str, Any]:
        sound = data.get('sound')
        distance = data.get('distance')

        if sound == 'siren':
            if distance == 'close':
                return {"action": "change_lane", "reason": "Emergency vehicle approaching"}
            else:
                return {"action": "slow_down_vehicle", "reason": "Potential emergency vehicle"}
        else:
            return {"action": "no_action", "reason": f"No specific action for {sound}"}


async def main():
    frame = Frame()
    config = FramerConfig(name="AutonomousVehicleFramer")
    framer = await frame.framer_factory.create_framer(config, plugins=frame.plugins)

    action_registry = ActionRegistry()
    action_registry.actions = {}
    action_registry.valid_actions = []

    execution_context = ExecutionContext(llm_service=framer.llm_service)
    execution_context.action_registry = action_registry
    execution_context.agency = framer.agency

    vehicle_plugin = AutonomousVehiclePlugin(framer)
    stop_vehicle_action = StopVehicleAction(vehicle_plugin)
    slow_down_vehicle_action = SlowDownVehicleAction(vehicle_plugin)
    change_lane_action = ChangeLaneAction(vehicle_plugin)
    process_perception_action = ProcessPerceptionAction(action_registry)

    action_registry.add_action(stop_vehicle_action)
    action_registry.add_action(slow_down_vehicle_action)
    action_registry.add_action(change_lane_action)
    action_registry.add_action(process_perception_action)

    framer.brain.action_registry = action_registry
    framer.execution_context = execution_context

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
        result = await action_registry.execute_action("process_perception", execution_context=execution_context, perception=perception)
        logger.info(f"Action result: {result}")
        await asyncio.sleep(1)

    await framer.close()


if __name__ == "__main__":
    asyncio.run(main())
