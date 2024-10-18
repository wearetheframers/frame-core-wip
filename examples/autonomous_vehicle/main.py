import sys
import os
import asyncio
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from frame import Frame, FramerConfig
from autonomous_vehicle_plugin import AutonomousVehiclePlugin
from frame.src.framer.agency.actions.base_action import Action
from frame.src.services.execution_context import ExecutionContext
from frame.src.framer.agency.priority import Priority
from frame.src.framer.agency.action_registry import ActionRegistry


class ProcessPerceptionAction(Action):
    """
    This replaces some default actions in our Framer like observe etc. 
    It is just meant as a custom function that allows low-level decision-making control
    suitable for a self-driving vehicle. It demonstrates the logic flow in perception processing
    and decision-making.
    """
    def __init__(self):
        super().__init__("process_perception", "Process a perception and make a decision", Priority.HIGH)

    async def execute(self, execution_context: ExecutionContext, perception: dict) -> str:
        print(f"\nProcessing perception: {perception}")
        decision = await execution_context.process_perception(perception)
        print(f"Decision made: {decision}")
        # The line below isn't necessary since we won't error when executing a null decision
        if decision:
            await execution_context.execute_decision(decision)
        return f"Processed perception: {perception['type']} - {perception['data']['object'] if 'object' in perception['data'] else perception['data']['sound']}"

async def main():
    frame = Frame()
    config = FramerConfig(name="AutonomousVehicleFramer")
    framer = await frame.create_framer(config)
    await framer.initialize()

    av_plugin = AutonomousVehiclePlugin()
    
    # This completely replaces the ActionRegistry and the default actions in the original Framer
    action_registry = ActionRegistry()

    # We must set our newly created Action Registry to our Framer's execution_context
    action_registry.execution_context = framer.brain.agency.execution_context
    action_registry.register_action(av_plugin.stop_vehicle, description="Stop the autonomous vehicle", priority=5)
    action_registry.register_action(av_plugin.slow_down_vehicle)
    action_registry.register_action(av_plugin.change_lane)

    process_perception_action = ProcessPerceptionAction()
    action_registry.register_action(process_perception_action)

    # Now we set our Framer's existing action_registry to our new action registry
    framer.brain.action_registry = action_registry

    # This behavior is desirable in this case as a self-driving vehicle has no need to do typical Framer responses
    # like research, respond, etc. and it is safer to keep actions to a minimal amount for a self-driving vehicle.

    perceptions = [
        {"type": "visual", "data": {"object": "stop sign", "distance": "far"}, "source": "camera"},
        {"type": "visual", "data": {"object": "stop sign", "distance": "close"}, "source": "camera"},
        {"type": "visual", "data": {"object": "pedestrian", "distance": "medium"}, "source": "camera"},
        {"type": "audio", "data": {"sound": "siren", "distance": "far"}, "source": "microphone"},
        {"type": "audio", "data": {"sound": "siren", "distance": "close"}, "source": "microphone"},
    ]

    for perception in perceptions:
        result = await action_registry.execute_action("process_perception", {"perception": perception})
        print(result)
        await asyncio.sleep(1)

    await framer.close()

if __name__ == "__main__":
    asyncio.run(main())
