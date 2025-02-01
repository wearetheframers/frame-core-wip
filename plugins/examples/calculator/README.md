# Calculator Plugin Example

## Overview

A simple calculator plugin that demonstrates the basic structure of a Frame plugin. This plugin provides basic arithmetic operations (add, subtract, multiply, divide) through actions, showing how to:

- Create a Frame plugin
- Register actions with different priorities
- Handle plugin execution
- Process parameters
- Return structured results

## Installation

The calculator plugin is included as an example in the Frame repository. No additional installation is needed.

## Requirements

No additional requirements - this plugin uses only Python standard library features.

## Usage

```python
from frame import Frame
from frame.framer.config import FramerConfig
from calculator_plugin import CalculatorPlugin

# Initialize Frame with the calculator plugin
frame = Frame()
config = FramerConfig(
    name="CalculatorFramer",
    permissions=["with_calculator"]
)
framer = await frame.create_framer(config)

# Initialize the plugin
calculator = CalculatorPlugin(framer)
await calculator.on_load()

# Perform calculations
result = await calculator.execute(
    "calculate_add",
    {"numbers": [1, 2, 3]}
)
print(f"Sum: {result['result']}")  # Output: Sum: 6
```

## Plugin Structure

The plugin consists of:

1. `calculator_plugin.py`: Main plugin implementation
2. `requirements.txt`: (Empty - no additional requirements)
3. `example.py`: Example usage script
4. `README.md`: This documentation

## Actions

The plugin provides these actions:

- `calculate_add`: Add a list of numbers
  ```python
  result = await calculator.execute("calculate_add", {"numbers": [1, 2, 3]})
  # Returns: {"result": 6, "numbers": [1, 2, 3], "operation": "add"}
  ```

- `calculate_subtract`: Subtract numbers sequentially
  ```python
  result = await calculator.execute("calculate_subtract", {"numbers": [10, 3, 2]})
  # Returns: {"result": 5, "numbers": [10, 3, 2], "operation": "subtract"}
  ```

- `calculate_multiply`: Multiply a list of numbers
  ```python
  result = await calculator.execute("calculate_multiply", {"numbers": [2, 3, 4]})
  # Returns: {"result": 24, "numbers": [2, 3, 4], "operation": "multiply"}
  ```

- `calculate_divide`: Divide numbers sequentially
  ```python
  result = await calculator.execute("calculate_divide", {"numbers": [100, 2, 2]})
  # Returns: {"result": 25.0, "numbers": [100, 2, 2], "operation": "divide"}
  ```

## Permissions

- `with_calculator`: Base permission required to use this plugin

## Development

This example demonstrates:

1. Basic plugin structure
2. Action registration
3. Parameter validation
4. Error handling
5. Result formatting

To extend this plugin:

1. Add new mathematical operations
2. Implement more complex calculations
3. Add validation for different number types
4. Include error logging
5. Add memory of previous calculations

## Testing

Run the example:

```bash
python example.py
```

## License

This plugin is released under the same license as Frame.
