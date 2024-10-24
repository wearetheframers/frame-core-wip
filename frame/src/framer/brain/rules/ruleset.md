# Ruleset Documentation

## Overview

A `Ruleset` is a collection of rules that guide decision-making within the `Framer` system. Each rule consists of a condition and an action. When the condition is met, the corresponding action is executed. This allows for dynamic and context-aware decision-making.

## How It Works

- **Condition**: A function that evaluates the current context and returns a boolean indicating whether the rule should be executed.
- **Action**: A function that is executed when the condition is met.

## Integration with Framer

In the `Framer` system, rulesets can be used to automate decision-making processes, allowing the agent to respond dynamically to changes in its environment. The `BasePlugin` class provides a method `add_rule` to add rules to the plugin's ruleset.

### Example Usage

```python
from frame.src.framer.brain.rules.ruleset import Ruleset, Rule

# Define a condition and an action
def condition(context):
    return context.get("temperature") > 30

def action(context):
    print("It's hot! Turning on the air conditioner.")

# Create a ruleset and add the rule
ruleset = Ruleset()
ruleset.add_rule(Rule(condition, action))

# Evaluate the ruleset with a context
context = {"temperature": 35}
ruleset.evaluate(context)
```

### Real-World Use Case

Rulesets can be used in smart home systems to automate actions based on environmental conditions, such as adjusting the thermostat or turning on lights.

## Components

- **Ruleset**: Manages a collection of rules and evaluates them against a given context.
- **Rule**: Represents a single rule with a condition and an action.

## Example in Framer

```python
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
```

This example demonstrates how to use the `BasePlugin` class with rule-based actions in a simple weather plugin.
