# Ruleset Documentation

## Overview

A `Ruleset` is a collection of rules that guide decision-making within the `Framer` system. Each rule consists of a condition and an action. When the condition is met, the corresponding action is executed. This allows for dynamic and context-aware decision-making.

## How It Works

- **Condition**: A function that evaluates the current context and returns a boolean indicating whether the rule should be executed.
- **Action**: A function that is executed when the condition is met.

## Example Usage

```python
from frame.src.framer.rules.ruleset import Ruleset, Rule

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

## Real-World Use Case

Rulesets can be used in smart home systems to automate actions based on environmental conditions, such as adjusting the thermostat or turning on lights.

## Integration with Frame/Framer

In the `Framer` system, rulesets can be used to automate decision-making processes, allowing the agent to respond dynamically to changes in its environment.
