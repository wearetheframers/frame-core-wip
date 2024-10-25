import aiohttp
from typing import Dict, Any
from frame.src.framer.brain.actions import BaseAction
from frame.src.services import ExecutionContext
from frame.src.framer.agency.priority import Priority


class WeatherPlugin:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"

    class GetWeatherAction(BaseAction):
        def __init__(self, plugin):
            super().__init__(
                "get_weather", "Get weather information for a city", Priority.MEDIUM
            )
            self.plugin = plugin

        async def execute(
            self, execution_context: ExecutionContext, query: str, location: str
        ) -> Dict[str, Any]:
            """
            Execute the action to get weather information for a given location.

            Args:
                execution_context (ExecutionContext): The execution context.
                query (str): The original query from the user.
                location (str): The location to get the weather for.

            Returns:
                Dict[str, Any]: A dictionary containing the response, data, and status.
            """
            params = {"q": location, "appid": self.plugin.api_key, "units": "metric"}
            async with aiohttp.ClientSession() as session:
                async with session.get(self.plugin.base_url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        weather_description = data["weather"][0]["description"]
                        temperature = data["main"]["temp"]
                        humidity = data["main"]["humidity"]
                        weather_summary = f"The weather in {location} is {weather_description}. Temperature: {temperature}°C, Humidity: {humidity}%"
                        return {
                            "response": f"Query: {query}\n{weather_summary}",
                            "data": data,
                            "status": response.status,
                        }
                    else:
                        return {
                            "response": f"Error: Unable to fetch weather data for {location}. Status code: {response.status}",
                            "data": None,
                            "status": response.status,
                        }

    def register_actions(self, action_registry):
        self.get_weather = self.GetWeatherAction(self)
        action_registry.add_action(self.get_weather)
        self.get_weather = self.GetWeatherAction(self)
        action_registry.add_action(self.get_weather)


import logging
from frame.src.framer.brain.plugins.base import BasePlugin
from frame.src.framer.agency.priority import Priority


class WeatherPlugin(BasePlugin):
    def __init__(self, framer=None):
        super().__init__(framer)
        self.logger = logging.getLogger(self.__class__.__name__)

    async def on_load(self, framer):
        self.framer = framer
        self.logger.info("WeatherPlugin loaded")
        self.register_actions(framer.brain.action_registry)

    def register_actions(self, action_registry):
        self.add_action(
            name="get_weather",
            action_func=self.get_weather,
            description="Retrieve the current weather for a specified city",
        )

    async def get_weather(self, execution_context, city: str) -> str:
        # Placeholder implementation for getting weather
        self.logger.info(f"Retrieving weather for city: {city}")
        return f"The weather in {city} is sunny with a high of 75°F."

    async def on_remove(self):
        self.logger.info("WeatherPlugin removed")

    async def execute(self, action: str, params: Dict[str, Any]) -> Any:
        if action == "get_weather":
            city = params.get("city", "unknown location")
            return await self.get_weather(self.execution_context, city)
        else:
            raise ValueError(f"Unknown action: {action}")
