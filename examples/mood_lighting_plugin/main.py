import asyncio
import os, sys

# Add the project root to the Python path to ensure all modules can be imported correctly
# If we are running the examples from the source code (not installing package from pip)
# then you need to have this line uncommented.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


from frame import Frame, FramerConfig
from mood_lighting_plugin import MoodLightingPlugin


async def main():
    # Initialize Frame
    frame = Frame()

    # Create a Framer instance with the MoodLightingPlugin
    config = FramerConfig(name="MoodLightingFramer", default_model="gpt-4o-mini")
    framer = await frame.create_framer(config)

    # Register the MoodLightingPlugin
    mood_lighting_plugin = MoodLightingPlugin(framer)
    framer.plugins["mood_lighting_plugin"] = mood_lighting_plugin

    # Simulate a mood change and adjust lighting
    mood = "happy"
    response = await framer.use_plugin_action(
        "mood_lighting_plugin",
        "adjust_lighting",
        {"execution_context": framer.execution_context, "mood": mood},
    )
    print(f"Lighting adjustment response: {response}")

    await framer.close()


if __name__ == "__main__":
    asyncio.run(main())
