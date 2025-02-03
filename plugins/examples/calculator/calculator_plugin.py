from frame.framer.brain.plugins.base import BasePlugin
from frame.framer.agency.priority import Priority
from typing import Dict, Any

class CalculatorPlugin(BasePlugin):
    """A simple calculator plugin demonstrating basic Frame plugin structure."""
    
    async def on_load(self):
        """Register calculator actions when plugin loads."""
        self.add_action(
            "calculate_add",
            self.add_numbers,
            "Add a list of numbers together",
            Priority.LOW
        )
        self.add_action(
            "calculate_subtract", 
            self.subtract_numbers,
            "Subtract numbers sequentially",
            Priority.LOW
        )
        self.add_action(
            "calculate_multiply",
            self.multiply_numbers, 
            "Multiply a list of numbers together",
            Priority.LOW
        )
        self.add_action(
            "calculate_divide",
            self.divide_numbers,
            "Divide numbers sequentially",
            Priority.LOW
        )

    async def add_numbers(self, numbers: list) -> float:
        """Add a list of numbers together."""
        return sum(numbers)

    async def subtract_numbers(self, numbers: list) -> float:
        """Subtract numbers sequentially."""
        result = numbers[0]
        for num in numbers[1:]:
            result -= num
        return result

    async def multiply_numbers(self, numbers: list) -> float:
        """Multiply a list of numbers together."""
        result = 1
        for num in numbers:
            result *= num
        return result

    async def divide_numbers(self, numbers: list) -> float:
        """Divide numbers sequentially."""
        result = numbers[0]
        for num in numbers[1:]:
            if num == 0:
                raise ValueError("Cannot divide by zero")
            result /= num
        return result

    async def execute(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the requested calculator action."""
        actions = {
            "calculate_add": self.add_numbers,
            "calculate_subtract": self.subtract_numbers,
            "calculate_multiply": self.multiply_numbers,
            "calculate_divide": self.divide_numbers
        }
        
        if action not in actions:
            raise ValueError(f"Unknown action: {action}")
            
        numbers = params.get("numbers", [])
        if not numbers or len(numbers) < 2:
            raise ValueError("At least two numbers are required")
            
        result = await actions[action](numbers)
        
        return {
            "result": result,
            "numbers": numbers,
            "operation": action.replace("calculate_", "")
        }
