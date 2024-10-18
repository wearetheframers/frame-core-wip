# Priority Enum Documentation

The `Priority` class is an enumeration that defines different levels of priority. It is used to assign a priority level to various tasks, roles, or goals within the system. The priority levels are defined as integer values, with higher numbers indicating higher priority.

## Priority Levels

- **LOWEST (1):** The lowest priority level.
- **VERY_LOW (2):** A very low priority level.
- **LOW (3):** A low priority level.
- **MEDIUM_LOW (4):** A medium-low priority level.
- **MEDIUM (5):** A medium priority level.
- **MEDIUM_HIGH (6):** A medium-high priority level.
- **HIGH (7):** A high priority level.
- **VERY_HIGH (8):** A very high priority level.
- **HIGHEST (9):** The highest priority level.
- **CRITICAL (10):** A critical priority level, indicating the utmost importance.

## Methods

### from_string(cls, value: Union[str, int]) -> "Priority"

Converts a string or integer value to a `Priority` enum member. If the input is a string, it is matched against predefined priority names. If the input is an integer, it is directly converted to the corresponding `Priority` member.

### from_value(cls, value: Union[int, str, "Priority"]) -> "Priority"

Converts a value to a `Priority` enum member. The input can be an integer, string, or another `Priority` instance. If the input is an integer, it is clamped between 1 and 10. If the input is a string, it is converted using the `from_string` method.

## Usage

The `Priority` enum is used throughout the system to standardize the representation of priority levels. It ensures that all components interpret priority levels consistently, facilitating effective decision-making and task management.
