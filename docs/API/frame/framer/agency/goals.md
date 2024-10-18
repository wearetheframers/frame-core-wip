# Goals

::: frame.src.framer.agency.goals.Goal
    options:
      show_root_heading: false
      show_source: false

## Overview

The `Goal` module is responsible for managing the objectives that guide the actions and decisions of a Framer. It provides mechanisms to define, update, and evaluate goals, ensuring that the Framer remains aligned with its intended purpose.

### Attributes

- `name` (str): The name of the goal.
- `description` (Optional[str]): A detailed description of the goal.
- `priority` (Priority): The priority level of the goal.
- `status` (GoalStatus): The current status of the goal (ACTIVE, COMPLETED, or ABANDONED).

## GoalStatus

::: frame.src.framer.agency.goals.GoalStatus
    options:
      show_root_heading: false
      show_source: false

An enumeration representing the possible statuses of a goal:

- `ACTIVE`: The goal is currently being pursued.
- `COMPLETED`: The goal has been achieved.
- `ABANDONED`: The goal is no longer being pursued.