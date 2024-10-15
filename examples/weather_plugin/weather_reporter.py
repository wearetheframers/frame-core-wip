import requests


class WeatherReporter:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"

    def get_weather(self, framer, city):
        params = {"q": city, "appid": self.api_key, "units": "metric"}
        response = requests.get(self.base_url, params=params)
        data = response.json()

        if response.status_code == 200:
            weather_description = data["weather"][0]["description"]
            temperature = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            return f"{framer.config.name}: The weather in {city} is {weather_description}. Temperature: {temperature}°C, Humidity: {humidity}%"
        else:
            return f"{framer.config.name}: Error: Unable to fetch weather data for {city}. Status code: {response.status_code}"
