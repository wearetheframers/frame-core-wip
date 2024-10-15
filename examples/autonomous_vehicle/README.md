# Autonomous Vehicle Example

This example demonstrates how to use the `Frame` and `Framer` classes to simulate an autonomous vehicle's decision-making process.

## Installation

To run this example, you need to have the `frame` package installed. You can install it using pip:

```bash
pip install frame
```

## Usage

Run the example script using Python:

```bash
python main.py
```

This will execute the example and simulate the decision-making process of an autonomous vehicle.

## Features

- Initializes a Framer instance with autonomous vehicle-specific configuration
- Uses an AutonomousVehiclePlugin to define vehicle-specific actions
- Simulates a series of perceptions (visual and audio inputs)
- Demonstrates how the Framer processes these perceptions and makes decisions
- Shows how the vehicle responds to different scenarios (stop signs, pedestrians, sirens)

## Note

This example uses asynchronous programming with `asyncio` to handle the simulation efficiently. Make sure you have a basic understanding of asynchronous Python to fully grasp the code structure.
