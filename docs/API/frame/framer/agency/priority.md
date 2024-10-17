# Priority

::: frame.src.models.framer.agency.priority.Priority
    options:
      show_root_heading: false
      show_source: false

## Overview

The `Priority` class is a Pydantic model that represents the priority of tasks, goals, or decisions within the Framer's agency. It provides a structured way to define and manage priorities.

### Attributes

- `level` (int): A numeric representation of the priority level. Range is 1-10, where 10 is the highest priority and 1 is the lowest.
- `name` (str): A short name or label for the priority level.
- `description` (Optional[str]): An optional detailed description of what the priority level means.

## Usage

To create a new Priority instance:

```python
from frame.src.models.framer.agency.priority import Priority

highest_priority = Priority(level=10, name="Critical", description="Extremely urgent and important tasks")
high_priority = Priority(level=8, name="High", description="Very important tasks")
medium_priority = Priority(level=5, name="Medium", description="Moderately important tasks")
low_priority = Priority(level=3, name="Low", description="Less important tasks")
lowest_priority = Priority(level=1, name="Lowest", description="Tasks with minimal importance")
```

To use Priority in other models or functions:

```python
def set_task_priority(task, priority: Priority):
    task.priority = priority
    print(f"Task priority set to {priority.name} (level {priority.level})")
    if priority.description:
        print(f"Description: {priority.description}")
```

Note: The Priority model itself doesn't include methods for setting, updating, or evaluating priorities. These operations would typically be handled by other components of the Framer's agency that use the Priority model.
# Priority

::: frame.src.models.framer.agency.priority.Priority
    options:
      show_root_heading: false
      show_source: false

## Overview

The `Priority` enum represents the priority levels that can be assigned to roles and goals within the Framer's agency. It provides a standardized way to define and manage priorities.

## Enum Values

- `LOWEST` = 1
- `VERY_LOW` = 2
- `LOW` = 3
- `MEDIUM_LOW` = 4
- `MEDIUM` = 5
- `MEDIUM_HIGH` = 6
- `HIGH` = 7
- `VERY_HIGH` = 8
- `HIGHEST` = 9
- `CRITICAL` = 10

## Methods

### `from_string`

This class method allows converting a string representation of priority to the corresponding `Priority` enum value.

```python
@classmethod
def from_string(cls, value: str) -> 'Priority':
    # Implementation details
```

## Usage

To use the Priority enum in roles or goals:

```python
from frame.src.models.framer.agency.priority import Priority

role = Role(
    name="Important Role",
    description="A role with high priority",
    priority=Priority.HIGH
)

goal = Goal(
    name="Critical Goal",
    description="A goal with the highest priority",
    priority=Priority.CRITICAL
)
```

The Priority enum helps in standardizing and managing the importance of different roles and goals within the Framer's agency, allowing for more nuanced decision-making and task prioritization.
