---
title: Plugins and Actions
weight: 50
---

Frame features a powerful and flexible plugin system inspired by game mods, allowing developers to extend the functionality of Framers. This system supports a community marketplace where plugins can be shared, sold, or given away, fostering a rich ecosystem of extensions and customizations. Plugins change Framer behaviors by adding or removing actions.

## Actions / Plugins

Actions in Frame are executable tasks that a Framer can perform. They are concrete implementations of tasks that can be executed in response to decisions made by the Framer. Actions are registered in the Framer's action registry and can be invoked directly by the Framer or automatically in its decision-making as it senses perceptions.

### Default Actions

Frame comes with a set of default actions that are available to all Framers. Actions can potentially lead to the creation of new actions. All default Framer actions can create new actions.

- **AdaptiveDecisionAction**: Makes decisions using an adaptive strategy based on context.
- **CreateNewAgentAction**: Creates new agents within the framework.
- **GenerateRolesAndGoalsAction**: Generates roles and goals for the Framer.
- **ObserveAction**: Processes observations and generates insights or actions.
- **RespondAction**: Generates a default response based on the current context.
- **ThinkAction**: Engages in deep thinking to generate new insights or tasks.
- **ResearchAction**: Conducts research to gather information.
- **ResourceAllocationAction**: Allocates resources based on urgency, risk, and available resources.

### Default Plugins

- **EQService**: Manages emotional intelligence aspects.
- **MemoryService**: Handles memory storage and retrieval.
- **SharedContext**: Manages shared context across components.
- **Mem0SearchExtractSummarizePlugin**: Enables memory retrieval and summarization.

### Permissions

By default, Framers have **no** access to default or installed plugins unless they are specified.

- **with_memory**: Allows access to memory services for storing and retrieving information. While Framer has access to memory by default, if you want it to respond with RAG-like features and automatically determine when to use memory retrieval versus responding without looking into any memories, you need to ensure the `with_mem0_search_extract_summarize` permission is enabled.
- **with_eq**: Enables emotional intelligence features for more nuanced interactions.
- **with_shared_context**: Provides access to shared context services for collaboration.

### Creating New Actions

To create a new action, follow these steps:

1. Define a new class that inherits from `BaseAction`.
2. Implement the `execute` method with the action's logic.
3. Register the action with the Framer's action registry.

Example:

```python
from frame.src.framer.brain.actions.base import BaseAction
from frame.src.services import ExecutionContext

class MyCustomAction(BaseAction):
    def __init__(self):
        # First param is name of action
        # Second param is description of action which is used for contextualizing when the Framer
        # should choose the action
        # Third param is the priority level of the action with 10 being the highest
        super().__init__("my_custom_action", "Description of the action", 3)

    async def execute(self, execution_context: ExecutionContext, **kwargs):
        # Implement action logic here
        return {"result": "Action executed successfully"}
```

### Example: Weather Forecast Plugin

Here's an example of how to develop, import, and run a plugin that provides weather forecasts:

1. **Create the Plugin**: Define a new plugin class in a Python file, e.g., `weather_plugin.py`.

```python
from frame.src.framer.brain.plugins.base import BasePlugin
from typing import Any, Dict

class WeatherPlugin(BasePlugin):
    async def on_load(self):
        self.add_action("get_weather", self.get_weather, "Fetch weather information for a location")

    async def execute(self, action: str, params: Dict[str, Any]) -> Any:
        if action == "get_weather":
            # Use the parse_location function to extract the location from natural language
            location = await self.parse_location(params.get("prompt"))
            return await self.get_weather(location)
        else:
            raise ValueError(f"Unknown action: {action}")

    async def parse_location(self, prompt: str) -> str:
        # Use Frame's get_completion method with LMQL prompt templating to parse location
        formatted_prompt = format_lmql_prompt(prompt, expected_output="location")
        response = await self.framer.get_completion(formatted_prompt)
        return response.strip()

    async def get_weather(self, location: str) -> str:
        # Example of fetching weather data from a real API
        import requests

        api_key = "your_api_key_here"
        base_url = "http://api.weatherapi.com/v1/current.json"
        response = requests.get(base_url, params={"key": api_key, "q": location})
        data = response.json()

        if "error" in data:
            return f"Error fetching weather data: {data['error']['message']}"
        
        weather = data["current"]["condition"]["text"]
        temperature = data["current"]["temp_c"]
        return f"Weather for {location}: {weather}, {temperature}C"
```

2. **Register the Plugin**: Import and register the plugin with a Framer instance.

```python
from frame import Frame, FramerConfig
from weather_plugin import WeatherPlugin

async def main():
    frame = Frame()
    config = FramerConfig(name="WeatherFramer", default_model="gpt-4o-mini")
    framer = await frame.create_framer(config)

    # Register the plugin
    weather_plugin = WeatherPlugin(framer)
    framer.plugins["weather_plugin"] = weather_plugin

    # Use the plugin with a prompt
    response = await framer.prompt("How's the weather today in NY?")
    print(f"Response using prompt: {response}")

    # Use the plugin with a sense method
    perception = {"type": "thought", "data": {"text": "I want to know what the weather is like in New York today since I am going there later."}}
    # Framer's decision making should prompt it to fetch the weather for the location
    decision = await framer.sense(perception)
    if decision:
        response = await framer.agency.execute_decision(decision)
        print(f"Response using sense: {response}")

    await framer.close()

asyncio.run(main())
```

The Framer intelligently chooses the best decision / action to take based on the perception (in this case a user message), conversational history, assigned roles, assigned goals, soul state, and the priority levels and descriptions of the other actions.

A plugin can also remove actions from the action registry whenever a plugin is loaded (though this could result in unexpected behavior for other plugins). This can help ensure more safe and restricted behavior, or enforce specific types of behavioral flows for the Framer. An example of this is in `examples/autonomous_vehicle/`.
