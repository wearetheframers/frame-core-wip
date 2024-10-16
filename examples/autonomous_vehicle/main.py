import sys
import os

# Import Frame from upper dir
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
import asyncio
from frame import Frame, FramerConfig
from autonomous_vehicle_plugin import AutonomousVehiclePlugin


async def main():
    # Initialize the Frame
    frame = Frame()

    # Initialize configuration
    config = FramerConfig(name="AutonomousVehicleFramer")

    # Create a Framer instance
    framer = await frame.create_framer(config)

    # Initialize the Framer (this will generate roles and goals if not provided)
    await framer.initialize()

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
            await framer.brain.execute_decision(decision)

        # Add a small delay to simulate time passing between perceptions
        await asyncio.sleep(1)

    # Clean up
    await frame.close()


# Run the example
if __name__ == "__main__":
    asyncio.run(main())
