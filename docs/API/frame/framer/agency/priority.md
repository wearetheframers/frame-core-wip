# Priority

::: frame.src.framer.agency.priority.Priority
    options:
      show_root_heading: true
      show_source: true

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
from frame.src.framer.agency.priority import Priority

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
