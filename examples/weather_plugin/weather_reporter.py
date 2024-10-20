import aiohttp
from frame.src.framer.brain.actions import BaseAction
from frame.src.services.execution_context import ExecutionContext
from frame.src.framer.agency.priority import Priority


class WeatherReporter:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"

    class GetWeatherAction(BaseAction):
        def __init__(self, plugin):
            super().__init__(
                "get_weather", "Get weather information for a city", Priority.MEDIUM
            )
            self.plugin = plugin

        async def execute(self, execution_context: ExecutionContext, city: str) -> str:
            params = {"q": city, "appid": self.plugin.api_key, "units": "metric"}
            async with aiohttp.ClientSession() as session:
                async with session.get(self.plugin.base_url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        weather_description = data["weather"][0]["description"]
                        temperature = data["main"]["temp"]
                        humidity = data["main"]["humidity"]
                        return f"{execution_context.framer.config.name}: The weather in {city} is {weather_description}. Temperature: {temperature}°C, Humidity: {humidity}%"
                    else:
                        return f"{execution_context.framer.config.name}: Error: Unable to fetch weather data for {city}. Status code: {response.status}"

    def register_actions(self, action_registry):
        self.get_weather = self.GetWeatherAction(self)
        action_registry.register_action(self.get_weather)
