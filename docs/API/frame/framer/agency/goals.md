# Goals

::: frame.src.framer.agency.goals.Goals
    options:
      show_root_heading: false
      show_source: false

## Overview

The `Goals` module is responsible for managing the objectives that guide the actions and decisions of a Framer. It provides mechanisms to define, update, and evaluate goals, ensuring that the Framer remains aligned with its intended purpose.

### Attributes

- `goal_list` (List[Goal]): A list of Goal objects representing the Framer's current goals.

## Goal

::: frame.src.models.framer.agency.goals.Goal
    options:
      show_root_heading: false
      show_source: false

### Attributes

- `name` (str): The name of the goal.
- `description` (Optional[str]): A detailed description of the goal.
- `priority` (Priority): The priority level of the goal.
- `status` (GoalStatus): The current status of the goal (ACTIVE, COMPLETED, or ABANDONED).

## GoalStatus

::: frame.src.models.framer.agency.goals.GoalStatus
    options:
      show_root_heading: false
      show_source: false

An enumeration representing the possible statuses of a goal:

- `ACTIVE`: The goal is currently being pursued.
- `COMPLETED`: The goal has been achieved.
- `ABANDONED`: The goal is no longer being pursued.

## Methods

### `add_goal`

Adds a new goal to the list of goals.

### `remove_goal`

Removes a goal from the list by its name.

### `evaluate_goals`

Evaluates the current goals to determine their relevance and priority.

## Usage

To add a new goal:

```python
from frame.src.models.framer.agency.goals import Goal, GoalStatus

new_goal = Goal(
    name="Increase Efficiency",
    description="Optimize processes to save time",
    priority=8,
    status=GoalStatus.ACTIVE
)
goals.add_goal(new_goal)
```

To evaluate goals:

```python
goals.evaluate_goals()
```

Goals influence the Framer's decision-making process, with active goals having more impact than completed or abandoned ones. The Framer considers goal priorities and statuses when processing perceptions and making decisions.
