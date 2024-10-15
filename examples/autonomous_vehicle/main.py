import sys
import os
import asyncio

# Add the frame-core directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from frame.frame import Frame
from frame.src.framer.config import FramerConfig
from frame.src.services.llm.main import LLMService
from frame.src.framer.framer_factory import FramerFactory
from frame.src.framer.agency.tasks.workflow.workflow_manager import WorkflowManager
from autonomous_vehicle_plugin import AutonomousVehiclePlugin
from autonomous_vehicle_plugin import AutonomousVehiclePlugin


async def main():
    # Initialize the Frame
    frame = Frame()

    # Initialize services and components
    # We've already initialized our API keys in our `.env` file
    llm_service = LLMService()
    config = FramerConfig(name="AutonomousVehicleFramer")

    roles = ["Driver"]
    goals = ["Navigate safely"]

    framer_factory = FramerFactory(config, llm_service)
    framer = await framer_factory.create_framer(
        soul_seed="Autonomous Vehicle Soul", memory_service=None, eq_service=None
    )

    framer.agency.set_roles(roles)
    framer.agency.set_goals(goals)

    # Initialize and register the plugin
    av_plugin = AutonomousVehiclePlugin()
    framer.brain.action_registry.add_action("stop", av_plugin.stop_vehicle)
    framer.brain.action_registry.add_action("slow_down", av_plugin.slow_down_vehicle)
    framer.brain.action_registry.add_action("change_lane", av_plugin.change_lane)

    # Simulate perceptions
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

    # Process perceptions and make decisions
    for perception in perceptions:
        print(f"\nProcessing perception: {perception}")
        decision = await framer.sense(perception)
        print(f"Decision made: {decision}")

        if decision and decision.action != "default_action":
            action_method = getattr(av_plugin, decision.action, None)
            if action_method and asyncio.iscoroutinefunction(action_method):
                await action_method()
            elif action_method:
                action_method()
            else:
                print(f"Action '{decision.action}' not found in the plugin.")

        # If no action was taken based on the decision, perform default actions
        if decision.action == "default_action":
            if perception["type"] == "visual":
                if (
                    perception["data"]["object"] == "stop sign"
                    and perception["data"]["distance"] == "close"
                ):
                    if asyncio.iscoroutinefunction(av_plugin.stop_vehicle):
                        await av_plugin.stop_vehicle()
                    else:
                        av_plugin.stop_vehicle()
                elif perception["data"]["object"] == "pedestrian":
                    if asyncio.iscoroutinefunction(av_plugin.slow_down_vehicle):
                        await av_plugin.slow_down_vehicle()
                    else:
                        av_plugin.slow_down_vehicle()
            elif (
                perception["type"] == "audio"
                and perception["data"]["sound"] == "siren"
                and perception["data"]["distance"] == "close"
            ):
                if asyncio.iscoroutinefunction(av_plugin.change_lane):
                    await av_plugin.change_lane()
                else:
                    av_plugin.change_lane()

        # Add a small delay to simulate time passing between perceptions
        await asyncio.sleep(1)


# Run the example
if __name__ == "__main__":
    asyncio.run(main())
