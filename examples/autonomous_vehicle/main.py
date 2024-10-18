import sys
import os
import asyncio
from frame import Frame, FramerConfig
from autonomous_vehicle_plugin import AutonomousVehiclePlugin
from frame.src.framer.agency.actions.base_action import Action
from frame.src.services.execution_context import ExecutionContext
from frame.src.models.framer.agency.priority import Priority

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

class ProcessPerceptionAction(Action):
    def __init__(self):
        super().__init__("process_perception", "Process a perception and make a decision", Priority.HIGH)

    async def execute(self, execution_context: ExecutionContext, perception: dict) -> str:
        print(f"\nProcessing perception: {perception}")
        decision = await execution_context.framer.sense(perception)
        print(f"Decision made: {decision}")
        await execution_context.framer.brain.execute_decision(decision)
        return f"Processed perception: {perception['type']} - {perception['data']['object'] if 'object' in perception['data'] else perception['data']['sound']}"

async def main():
    frame = Frame()
    config = FramerConfig(name="AutonomousVehicleFramer")
    framer = await frame.create_framer(config)
    await framer.initialize()

    av_plugin = AutonomousVehiclePlugin()
    framer.brain.action_registry.register_action(av_plugin.stop_vehicle)
    framer.brain.action_registry.register_action(av_plugin.slow_down_vehicle)
    framer.brain.action_registry.register_action(av_plugin.change_lane)

    process_perception_action = ProcessPerceptionAction()
    framer.brain.action_registry.register_action(process_perception_action)

    perceptions = [
        {"type": "visual", "data": {"object": "stop sign", "distance": "far"}, "source": "camera"},
        {"type": "visual", "data": {"object": "stop sign", "distance": "close"}, "source": "camera"},
        {"type": "visual", "data": {"object": "pedestrian", "distance": "medium"}, "source": "camera"},
        {"type": "audio", "data": {"sound": "siren", "distance": "far"}, "source": "microphone"},
        {"type": "audio", "data": {"sound": "siren", "distance": "close"}, "source": "microphone"},
    ]

    for perception in perceptions:
        result = await framer.brain.action_registry.execute_action("process_perception", {"perception": perception})
        print(result)
        await asyncio.sleep(1)

    await framer.close()

if __name__ == "__main__":
    asyncio.run(main())
