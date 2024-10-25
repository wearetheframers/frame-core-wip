# Mood Lighting Plugin Example

This example demonstrates how to use the `MoodLightingPlugin` with the Frame framework to simulate a smart home lighting system that adjusts based on the Framer's emotional state.

## Setup

1. Ensure you have the necessary dependencies installed. You can install them using:

   ```bash
   pip install -r requirements.txt
   ```

2. Navigate to the `examples/mood_lighting_plugin` directory.

3. Run the main script to see the plugin in action:

   ```bash
   python main.py
   ```

## How It Works

- The `MoodLightingPlugin` is registered with a Framer instance.
- The plugin provides an action `adjust_lighting` that adjusts the lighting based on the Framer's mood.
- The main script simulates a mood change to "happy" and calls the `adjust_lighting` action to adjust the lighting accordingly.

## Customization

You can customize the plugin to handle different moods and adjust the lighting in various ways. Modify the `adjust_lighting` method in `mood_lighting_plugin.py` to add more moods and lighting settings.

## License

This example is provided under the MIT License. See the LICENSE file for more details.
