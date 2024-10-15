import aiohttp
import asyncio


class WeatherReporter:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"

    async def get_weather(self, framer, city):
        params = {"q": city, "appid": self.api_key, "units": "metric"}
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    weather_description = data["weather"][0]["description"]
                    temperature = data["main"]["temp"]
                    humidity = data["main"]["humidity"]
                    return f"{framer.config.name}: The weather in {city} is {weather_description}. Temperature: {temperature}°C, Humidity: {humidity}%"
                else:
                    return f"{framer.config.name}: Error: Unable to fetch weather data for {city}. Status code: {response.status}"
