# Goals

::: frame.src.framer.agency.goals.Goals
    options:
      show_root_heading: false
      show_source: false

## Overview

The `Goals` module is responsible for managing the objectives that guide the actions and decisions of a Framer. It provides mechanisms to define, update, and evaluate goals, ensuring that the Framer remains aligned with its intended purpose.

### Attributes

- `goal_list` (List[Dict[str, Any]]): A list of goals with their descriptions and priorities.

## Methods

### `add_goal`

Adds a new goal to the list of goals.

### `remove_goal`

Removes a goal from the list by its identifier.

### `evaluate_goals`

Evaluates the current goals to determine their relevance and priority.

## Usage

To add a new goal:

```python
goals.add_goal(
    {"name": "Increase Efficiency", "description": "Optimize processes to save time", "priority": 3}
)
```

To evaluate goals:

```python
relevant_goals = goals.evaluate_goals()
```
