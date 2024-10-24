# Strategy Pattern Example

This example demonstrates how to use the Strategy Pattern within the Frame framework to make adaptive decisions based on varying contexts. The Strategy Pattern is a behavioral design pattern that enables selecting an algorithm's behavior at runtime. It is particularly useful in scenarios where you need to choose between different strategies based on the current context or environment.

## Understanding the Strategy Pattern

The Strategy Pattern is a design pattern that allows you to define a family of algorithms, encapsulate each one, and make them interchangeable. This pattern is particularly useful when you need to switch between different strategies based on the context or environment.

In this example, we demonstrate how to use the Strategy Pattern within the Frame framework to make adaptive decisions based on varying contexts. The `AdaptiveDecisionAction` class employs different strategies to make decisions based on the urgency and risk levels of a given context.

In this example, we use the `AdaptiveDecisionAction` class, which employs different strategies to make decisions based on the urgency and risk levels of a given context. The strategies include:

- **ConservativeStrategy**: Used when resources are abundant and risk is low, favoring cautious decision-making.
- **AggressiveStrategy**: Used when urgency is high or resources are scarce, favoring quick and decisive actions.
- **BalancedStrategy**: Used when multiple factors are moderate, favoring a balanced approach.

## Integration with Rules

While the Strategy Pattern focuses on selecting algorithms at runtime, it can be effectively combined with rule-based systems to enhance decision-making. In the Frame framework, rules can be used to determine which strategy to apply based on the current context. For example, a rule might dictate that if the urgency is above a certain threshold, the `AggressiveStrategy` should be used. This integration allows for more dynamic and context-aware decision-making processes.

## Why Use the Strategy Pattern?

The Strategy Pattern is beneficial in scenarios where:

- You need to switch between different algorithms or strategies at runtime.
- You want to encapsulate different behaviors and make them interchangeable.
- You aim to adhere to the Open/Closed Principle by allowing new strategies to be added without modifying existing code.

## Real-World Scenarios and Use Cases

1. **Autonomous Vehicles**: An autonomous vehicle might use different driving strategies based on road conditions. For instance, it could drive conservatively in bad weather, aggressively in clear conditions, and balanced in normal conditions.

2. **Financial Trading**: A trading bot might switch between aggressive trading strategies during high volatility and conservative strategies during stable market conditions.

3. **Resource Management**: In cloud computing, a system might allocate resources aggressively when demand is high and conservatively when resources are limited.

4. **Healthcare Management**: In a hospital setting, different strategies can be employed for patient management based on the urgency of care required and available resources.

5. **Supply Chain Optimization**: Companies can use different strategies to manage inventory and logistics based on market demand and supply chain disruptions.

## Custom Plugins and Unique Real-World Use Cases

### Plugin for Environmental Monitoring

This plugin uses the Strategy Pattern to adaptively manage energy consumption based on environmental conditions.

```python
from frame.src.framer.brain.plugins import BasePlugin
from typing import Dict, Any

class EnvironmentalMonitoringPlugin(BasePlugin):
    async def on_load(self):
        self.add_rule(self.is_peak_hour, self.activate_energy_saving)

    def is_peak_hour(self, context: Dict[str, Any]) -> bool:
        return context.get("time_of_day") in ["morning", "evening"]

    def activate_energy_saving(self, context: Dict[str, Any]) -> None:
        print("Activating energy-saving strategies.")

# Example usage
import asyncio
from frame import Frame, FramerConfig

async def main():
    # Initialize Frame
    frame = Frame()

    # Create a Framer instance
    config = FramerConfig(name="EnvironmentalFramer", default_model="gpt-4o-mini")
    framer = await frame.create_framer(config)

    # Initialize and load the plugin
    plugin = EnvironmentalMonitoringPlugin(framer)
    await plugin.on_load()

    # Define a context for peak hours
    context = {"time_of_day": "morning"}
    plugin.evaluate_rules(context, "activate_energy_saving")

    await framer.close()

if __name__ == "__main__":
    asyncio.run(main())
```

### Plugin for Personalized Education

This plugin adapts teaching methods based on the student's learning style.

```python
from frame.src.framer.brain.plugins import BasePlugin
from typing import Dict, Any

class PersonalizedEducationPlugin(BasePlugin):
    async def on_load(self):
        self.add_rule(self.is_visual_learner, self.use_visual_teaching)

    def is_visual_learner(self, context: Dict[str, Any]) -> bool:
        return context.get("learning_style") == "visual"

    def use_visual_teaching(self, context: Dict[str, Any]) -> None:
        print("Using visual teaching methods.")

# Example usage
import asyncio
from frame import Frame, FramerConfig

async def main():
    # Initialize Frame
    frame = Frame()

    # Create a Framer instance
    config = FramerConfig(name="EducationFramer", default_model="gpt-4o-mini")
    framer = await frame.create_framer(config)

    # Initialize and load the plugin
    plugin = PersonalizedEducationPlugin(framer)
    await plugin.on_load()

    # Define a context for a visual learner
    context = {"learning_style": "visual"}
    plugin.evaluate_rules(context, "use_visual_teaching")

    await framer.close()

if __name__ == "__main__":
    asyncio.run(main())
```

### Plugin for Dynamic Marketing Campaigns

This plugin adjusts marketing strategies based on customer engagement levels.

```python
from frame.src.framer.brain.plugins import BasePlugin
from typing import Dict, Any

class DynamicMarketingPlugin(BasePlugin):
    async def on_load(self):
        self.add_rule(self.is_high_engagement, self.run_aggressive_campaign)

    def is_high_engagement(self, context: Dict[str, Any]) -> bool:
        return context.get("engagement_level") > 7

    def run_aggressive_campaign(self, context: Dict[str, Any]) -> None:
        print("Running aggressive marketing campaign.")

# Example usage
import asyncio
from frame import Frame, FramerConfig

async def main():
    # Initialize Frame
    frame = Frame()

    # Create a Framer instance
    config = FramerConfig(name="MarketingFramer", default_model="gpt-4o-mini")
    framer = await frame.create_framer(config)

    # Initialize and load the plugin
    plugin = DynamicMarketingPlugin(framer)
    await plugin.on_load()

    # Define a context for high engagement
    context = {"engagement_level": 8}
    plugin.evaluate_rules(context, "run_aggressive_campaign")

    await framer.close()

if __name__ == "__main__":
    asyncio.run(main())
```

### Plugin for Environmental Monitoring

```python
from frame.src.framer.brain.plugins import BasePlugin
from typing import Dict, Any

class EnvironmentalMonitoringPlugin(BasePlugin):
    async def on_load(self):
        self.add_rule(self.is_peak_hour, self.activate_energy_saving)

    def is_peak_hour(self, context: Dict[str, Any]) -> bool:
        return context.get("time_of_day") in ["morning", "evening"]

    def activate_energy_saving(self, context: Dict[str, Any]) -> None:
        print("Activating energy-saving strategies.")

# Example usage
if __name__ == "__main__":
    # Create a mock Framer instance
    class MockFramer:
        def __init__(self):
            self.execution_context = None

    framer = MockFramer()
    plugin = EnvironmentalMonitoringPlugin(framer)

    # Simulate loading the plugin
    import asyncio
    asyncio.run(plugin.on_load())

    # Define a context for peak hours
    context = {"time_of_day": "morning"}
    plugin.evaluate_rules(context, "activate_energy_saving")
```

### Plugin for Personalized Education

```python
from frame.src.framer.brain.plugins import BasePlugin
from typing import Dict, Any

class PersonalizedEducationPlugin(BasePlugin):
    async def on_load(self):
        self.add_rule(self.is_visual_learner, self.use_visual_teaching)

    def is_visual_learner(self, context: Dict[str, Any]) -> bool:
        return context.get("learning_style") == "visual"

    def use_visual_teaching(self, context: Dict[str, Any]) -> None:
        print("Using visual teaching methods.")

# Example usage
if __name__ == "__main__":
    # Create a mock Framer instance
    class MockFramer:
        def __init__(self):
            self.execution_context = None

    framer = MockFramer()
    plugin = PersonalizedEducationPlugin(framer)

    # Simulate loading the plugin
    import asyncio
    asyncio.run(plugin.on_load())

    # Define a context for a visual learner
    context = {"learning_style": "visual"}
    plugin.evaluate_rules(context, "use_visual_teaching")
```

### Plugin for Dynamic Marketing Campaigns

```python
from frame.src.framer.brain.plugins import BasePlugin
from typing import Dict, Any

class DynamicMarketingPlugin(BasePlugin):
    async def on_load(self):
        self.add_rule(self.is_high_engagement, self.run_aggressive_campaign)

    def is_high_engagement(self, context: Dict[str, Any]) -> bool:
        return context.get("engagement_level") > 7

    def run_aggressive_campaign(self, context: Dict[str, Any]) -> None:
        print("Running aggressive marketing campaign.")

# Example usage
if __name__ == "__main__":
    # Create a mock Framer instance
    class MockFramer:
        def __init__(self):
            self.execution_context = None

    framer = MockFramer()
    plugin = DynamicMarketingPlugin(framer)

    # Simulate loading the plugin
    import asyncio
    asyncio.run(plugin.on_load())

    # Define a context for high engagement
    context = {"engagement_level": 8}
    plugin.evaluate_rules(context, "run_aggressive_campaign")
```

### Plugin for Smart Home Automation

```python
from frame.src.framer.brain.plugins import BasePlugin
from typing import Dict, Any

class SmartHomeAutomationPlugin(BasePlugin):
    async def on_load(self):
        self.add_rule(self.is_night_time, self.adjust_lighting)

    def is_night_time(self, context: Dict[str, Any]) -> bool:
        return context.get("time_of_day") == "night"

    def adjust_lighting(self, context: Dict[str, Any]) -> None:
        print("Adjusting lighting for night time.")

# Example usage
if __name__ == "__main__":
    # Create a mock Framer instance
    class MockFramer:
        def __init__(self):
            self.execution_context = None

    framer = MockFramer()
    plugin = SmartHomeAutomationPlugin(framer)

    # Simulate loading the plugin
    import asyncio
    asyncio.run(plugin.on_load())

    # Define a context for night time
    context = {"time_of_day": "night"}
    plugin.evaluate_rules(context, "adjust_lighting")
```

### Plugin for Adaptive Security Systems

```python
from frame.src.framer.brain.plugins import BasePlugin
from typing import Dict, Any

class AdaptiveSecurityPlugin(BasePlugin):
    async def on_load(self):
        self.add_rule(self.is_high_risk, self.activate_aggressive_monitoring)

    def is_high_risk(self, context: Dict[str, Any]) -> bool:
        return context.get("threat_level") > 5

    def activate_aggressive_monitoring(self, context: Dict[str, Any]) -> None:
        print("Activating aggressive security monitoring.")

# Example usage
if __name__ == "__main__":
    # Create a mock Framer instance
    class MockFramer:
        def __init__(self):
            self.execution_context = None

    framer = MockFramer()
    plugin = AdaptiveSecurityPlugin(framer)

    # Simulate loading the plugin
    import asyncio
    asyncio.run(plugin.on_load())

    # Define a context for high threat level
    context = {"threat_level": 6}
    plugin.evaluate_rules(context, "activate_aggressive_monitoring")
```

## Conclusion

1. **Autonomous Vehicles**: An autonomous vehicle might use different driving strategies based on road conditions. For instance, it could drive conservatively in bad weather, aggressively in clear conditions, and balanced in normal conditions.

2. **Financial Trading**: A trading bot might switch between aggressive trading strategies during high volatility and conservative strategies during stable market conditions.

3. **Resource Management**: In cloud computing, a system might allocate resources aggressively when demand is high and conservatively when resources are limited.

## Handling Incomplete Contexts

In cases where the perception lacks detailed information such as stakeholders, risk, or urgency, the `AdaptiveDecisionAction` is designed to extrapolate and quantify these factors. The Brain component will attempt to infer missing details based on available context, historical data, and perception data. This allows the system to make informed decisions even with incomplete information.

The extrapolation process involves:
- Analyzing available context and perception data to estimate missing factors.
- Using historical data and patterns to infer risk and urgency levels.
- Making decisions based on the best available extrapolated data.

This approach ensures that the system remains flexible and adaptive, capable of making decisions in a wide range of scenarios.

### Step 1: Define Your Strategies

First, define the strategies you want to use. In this example, we have three strategies: `ConservativeStrategy`, `AggressiveStrategy`, and `BalancedStrategy`.

### Step 2: Implement the AdaptiveDecisionAction

The `AdaptiveDecisionAction` class uses these strategies to make decisions based on the context. It selects the appropriate strategy based on the urgency and risk levels.

### Step 3: Use the AdaptiveDecisionAction

Create a Framer instance and register the `AdaptiveDecisionAction`. Then, define various contexts and use the action to make decisions.

## Running the Example

### Prerequisites

Ensure you have Python installed on your system. You will also need to install the required dependencies. You can do this by running:

```bash
pip install -r requirements.txt
```

### Running the Simulation

To run the trading simulation example, execute the following command in your terminal:

```bash
python trading_simulation.py
```

This will initialize the Frame and Framer, register the `AdaptiveDecisionAction`, and process a series of scenarios to demonstrate how different strategies are selected based on the context.

### Understanding the Output

The output will display the context for each scenario and the corresponding decision made by the `AdaptiveDecisionAction`. This will help you understand how the strategy pattern is applied in real-time decision-making.

## Conclusion

The Strategy Pattern is a powerful tool for creating flexible and adaptive systems. By using the `AdaptiveDecisionAction` in Frame, you can implement dynamic decision-making processes that respond to changing conditions in real-time. This example provides a foundation for building more complex and responsive AI agents using the Strategy Pattern.
