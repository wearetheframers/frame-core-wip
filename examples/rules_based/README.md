# Plugin Example

This example demonstrates how to use the `BasePlugin` class with rule-based actions in a simple weather plugin.

## Overview

The `WeatherPlugin` is a simple plugin that checks the weather condition and suggests taking an umbrella if it is raining. It uses the `BasePlugin` class to define rules and actions.

## Files

- `main.py`: The main script that demonstrates the usage of the `WeatherPlugin`.
- `plugin_rule_example.py`: An additional example showing how to create and use a plugin with rules.

## Running the Example

To run the example, execute the following command:

```bash
python main.py
```

## Explanation

1. **WeatherPlugin**: A plugin that defines a rule to check if it is raining and an action to take an umbrella.
2. **Rules and Actions**: The plugin uses the `add_rule` method to add a rule that checks the weather condition and executes the `take_umbrella` action if it is raining.
3. **Contexts**: The example evaluates the rules for different weather contexts to demonstrate the plugin's behavior.

## Additional Examples

- `plugin_rule_example.py`: This file provides another example of using the `BasePlugin` class with rules. It shows how to create a plugin, add rules, and evaluate them based on the context.
