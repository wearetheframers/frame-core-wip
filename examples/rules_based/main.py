import asyncio
from typing import Dict, Any

import os, sys

# Add the project root to the Python path to ensure all modules can be imported correctly
# If we are running the examples from the source code (not installing package from pip)
# then you need to have this line uncommented.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from frame.src.framer.brain.plugins import BasePlugin


class WeatherPlugin(BasePlugin):
    """
    A plugin that provides weather-related actions and rules.
    """

    async def on_load(self):
        """
        Load the plugin and add rules.
        """
        self.add_rule(self.is_raining, self.take_umbrella)

    def is_raining(self, context: Dict[str, Any]) -> bool:
        """
        Check if the weather is raining.

        Args:
            context (Dict[str, Any]): The current context.

        Returns:
            bool: True if it is raining, False otherwise.
        """
        return context.get("weather") == "rain"

    def take_umbrella(self, context: Dict[str, Any]) -> None:
        """
        Action to take an umbrella.

        Args:
            context (Dict[str, Any]): The current context.
        """
        print("It's raining. Take an umbrella!")


async def main():
    # Create a mock Framer instance
    class MockFramer:
        def __init__(self):
            self.execution_context = None

    framer = MockFramer()
    plugin = WeatherPlugin(framer)

    # Simulate loading the plugin
    await plugin.on_load()

    # Define contexts for different weather conditions
    contexts = [{"weather": "rain"}, {"weather": "sunny"}, {"weather": "cloudy"}]

    # Evaluate rules for each context
    for context in contexts:
        print(f"Evaluating context: {context}")
        plugin.evaluate_rules(context, "take_umbrella")


if __name__ == "__main__":
    asyncio.run(main())
