import asyncio
import os, sys

# Add the project root to the Python path to ensure all modules can be imported correctly
# If we are running the examples from the source code (not installing package from pip)
# then you need to have this line uncommented.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from frame.frame import Frame
from frame.src.framer.config import FramerConfig
from frame.src.services.llm.main import LLMService
from frame.src.framer.framer_factory import FramerFactory
from plugins.weather_plugin import WeatherPlugin

async def main():
    # Initialize the Frame
    frame = Frame()

    # Initialize services and components
    llm_service = LLMService()
    config = FramerConfig(name="WeatherFramer")

    roles = ["Weather Assistant"]
    goals = ["Provide accurate weather information"]

    framer_factory = FramerFactory(config, llm_service)
    framer = await framer_factory.create_framer(
        memory_service=None, eq_service=None
    )

    await framer.initialize()  # Initialize roles and goals

    # Initialize and register the plugin
    weather_api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    if not weather_api_key:
        raise ValueError("OPENWEATHERMAP_API_KEY environment variable is not set")

    weather_plugin = WeatherPlugin(weather_api_key)
    weather_plugin.register_actions(framer.brain.action_registry)

    # Simulate perceptions
    perceptions = [
        {
            "type": "text",
            "data": {"content": "What's the weather like in New York?"},
            "source": "user",
        },
        {
            "type": "text",
            "data": {"content": "Is it going to rain in London tomorrow?"},
            "source": "user",
        },
        {
            "type": "text",
            "data": {"content": "What's the temperature in Tokyo right now?"},
            "source": "user",
        },
    ]

    # Process perceptions and make decisions
    for perception in perceptions:
        print(f"\nProcessing perception: {perception}")
        decision = await framer.sense(perception)
        print(f"Decision made: {decision}")

        if decision:
            # Extract the city/location from the perception data
            city = perception["data"]["content"].split("in")[-1].strip("?").strip()
            await framer.brain.execute_decision(decision, query=perception["data"]["content"], location=city)

        # Add a small delay to simulate time passing between perceptions
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
