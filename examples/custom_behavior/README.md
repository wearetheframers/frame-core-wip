# Custom Behavior Example

This example demonstrates how to create and use a custom action within the Frame framework. The custom action, `custom_greet`, is designed to greet a user with a custom message and is registered with a high priority to ensure it is preferred over other actions.

## How It Works

- **Custom Action**: The `custom_greet_action` function is defined to take a custom message and an optional name parameter. It returns a greeting message.
- **Action Registration**: The custom action is registered with the Framer's action registry with a high priority, ensuring it is chosen over default actions like `respond`.
- **Decision Making**: The Framer's brain makes a decision based on the input data, and if the action is `custom_greet`, it executes the custom action.

## What It Does

The script initializes a Framer instance, registers the custom action, and demonstrates its usage by making a decision and executing the custom action. The result is printed to the console.

## How to Run

1. Ensure you have the necessary dependencies installed. You can install them using:
   ```bash
   pip install -r requirements.txt
   ```

2. Navigate to the `examples/custom_behavior` directory.

3. Run the script using Python:
   ```bash
   python main.py
   ```

4. The output will display the result of the custom greet action.

## Cleanup

The script includes a cleanup section to release any resources used during execution.
