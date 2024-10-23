from frame.src.framer.brain.plugins import BasePlugin
from typing import Dict, Any


class WeatherPlugin(BasePlugin):
    async def on_load(self):
        self.add_rule(self.is_raining, self.take_umbrella)

    def is_raining(self, context: Dict[str, Any]) -> bool:
        return context.get("weather") == "rain"

    def take_umbrella(self, context: Dict[str, Any]) -> None:
        print("It's raining. Take an umbrella!")


# Example usage
if __name__ == "__main__":
    # Create a mock Framer instance
    class MockFramer:
        def __init__(self):
            self.execution_context = None

    framer = MockFramer()
    plugin = WeatherPlugin(framer)

    # Simulate loading the plugin
    import asyncio

    asyncio.run(plugin.on_load())

    # Define a context where it's raining
    context = {"weather": "rain"}

    # Evaluate rules with the given context
    plugin.evaluate_rules(context, "take_umbrella")
