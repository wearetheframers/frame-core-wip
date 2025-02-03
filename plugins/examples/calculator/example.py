import sys
import os
import asyncio

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from frame import Frame
from frame.framer.config import FramerConfig
from calculator_plugin import CalculatorPlugin

async def main():
    # Initialize Frame
    frame = Frame()
    
    # Create a Framer with calculator permissions
    config = FramerConfig(
        name="CalculatorFramer",
        permissions=["with_calculator"]
    )
    framer = await frame.create_framer(config)

    # Initialize and register the calculator plugin
    calculator = CalculatorPlugin(framer)
    await calculator.on_load()

    # Example calculations
    calculations = [
        ("calculate_add", [1, 2, 3, 4, 5]),
        ("calculate_subtract", [100, 20, 30]),
        ("calculate_multiply", [2, 3, 4]),
        ("calculate_divide", [100, 2, 2])
    ]

    for action, numbers in calculations:
        try:
            result = await calculator.execute(action, {"numbers": numbers})
            print(f"\nAction: {action}")
            print(f"Numbers: {numbers}")
            print(f"Result: {result['result']}")
        except Exception as e:
            print(f"Error in {action}: {str(e)}")

    await framer.close()

if __name__ == "__main__":
    asyncio.run(main())
