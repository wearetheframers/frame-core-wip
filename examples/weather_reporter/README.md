# Weather Plugin Example

This example demonstrates how to use the `WeatherReporter` class to fetch and process weather data asynchronously.

## Installation

To run this example, you need to have the `aiohttp` package installed. You can install it using pip:

```bash
pip install aiohttp
```

## Usage

Run the example script using Python:

```bash
python main.py
```

This will execute the example and demonstrate how to fetch weather data for specified cities using the OpenWeatherMap API asynchronously.

## Environment Variables

Make sure to set the `OPENWEATHERMAP_API_KEY` environment variable with your OpenWeatherMap API key before running the script.

```bash
export OPENWEATHERMAP_API_KEY=your_api_key_here
```

## Note

This example uses asynchronous programming with `asyncio` and `aiohttp` to efficiently handle multiple weather requests concurrently.
