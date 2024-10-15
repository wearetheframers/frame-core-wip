import asyncio
import os
from frame.frame import Frame
from frame.src.framer.config import FramerConfig
from frame.src.services.llm.main import LLMService
from frame.src.framer.framer_factory import FramerFactory
from weather_plugin import WeatherPlugin


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
        soul_seed="Weather Assistant Soul", memory_service=None, eq_service=None
    )

    framer.set_roles(roles)
    framer.set_goals(goals)

    # Initialize and register the plugin
    weather_api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    if not weather_api_key:
        raise ValueError("OPENWEATHERMAP_API_KEY environment variable is not set")

    weather_plugin = WeatherPlugin(weather_api_key)
    framer.brain.action_registry.add_action("get_weather", weather_plugin.get_weather)

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
        decision = await framer.process_perception(perception)
        print(f"Decision made: {decision}")

        if decision:
            await framer.brain.execute_decision(decision)

        # Add a small delay to simulate time passing between perceptions
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
