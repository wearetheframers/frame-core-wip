# Import necessary modules and packages
import sys
import logging
import warnings

# Suppress specific FutureWarning from torch.load
warnings.filterwarnings("ignore", category=FutureWarning, module="whisper")
import os
import asyncio
from typing import Dict, Any

# Add the project root to the Python path to ensure all modules can be imported correctly
# If we are running the examples from the source code (not installing package from pip)
# then you need to have this line uncommented.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from frame import Frame, FramerConfig
from autonomous_vehicle_plugin import (
    StopVehicleAction,
    SlowDownVehicleAction,
    SpeedUpVehicleAction,
    ChangeLaneAction,
    StartDrivingAction,
    NoActionAction,
    BrakeVehicleAction,
    AutonomousVehiclePlugin,
)
from frame.src.framer.brain.actions import BaseAction
from frame.src.framer.agency.priority import Priority
from frame.src.framer.brain.action_registry import ActionRegistry
from frame.src.services.context.execution_context_service import ExecutionContext

# Set up logging for the module
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)
logger.addHandler(handler)


# Define a custom action to process perceptions and make decisions
class ProcessPerceptionAction(BaseAction):
    # Note: The process_perception function is separate from the plugin to demonstrate flexibility,
    # in how you can add actions to a plugin or from outside a plugin.

    def __init__(self, action_registry: ActionRegistry):
        super().__init__(
            "process_perception",
            "Process a perception and make a decision",
            Priority.HIGH,
        )
        self.action_registry = action_registry

    # Execute the action based on the given perception
    async def execute(self, execution_context: ExecutionContext, **kwargs) -> str:
        # Retrieve the perception from the provided arguments
        perception = kwargs.get("perception")

        if not perception:
            return "Error: Missing perception"

        logger.info(f"\nProcessing perception: {perception}")

        # Analyze the perception and make a decision based on its type and data
        decision = self.analyze_perception(perception)
        logger.info(f"Decision made: {decision}")

        # Execute the decision using the action registry
        result = await self.execute_decision(execution_context, decision)
        return str(result)

    async def execute_decision(
        self, execution_context: ExecutionContext, decision: Dict[str, Any]
    ) -> str:
        action = decision.get("action")
        if action == "no_action":
            return f"No action taken: {decision.get('reason')}"

        try:
            result = await self.action_registry.execute_action(action, **decision)
            return f"Executed {action}: {result}"
        except Exception as e:
            return f"Error executing action {action}: {str(e)}"

    # Analyze the perception to determine the appropriate action
    def analyze_perception(self, perception: Dict[str, Any]) -> Dict[str, Any]:
        # Determine the type of perception and handle accordingly
        perception_type = perception.get("type")
        data = perception.get("data", {})

        if perception_type == "visual":
            return self.handle_visual_perception(data)
        elif perception_type == "audio":
            return self.handle_audio_perception(data)
        elif perception_type == "traffic":
            return self.handle_traffic_perception(data)
        else:
            return {
                "action": "no_action",
                "reason": f"Unknown perception type: {perception_type}",
            }

    # Handle visual perceptions such as detecting objects and their distances
    def handle_visual_perception(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Determine the object type and distance to decide on an action
        object_type = data.get("object")
        distance = data.get("distance")

        if object_type == "stop sign":
            if distance == "close":
                return {"action": "stop_vehicle", "reason": "Stop sign is close"}
            else:
                return {
                    "action": "slow_down_vehicle",
                    "reason": "Approaching stop sign",
                }
        elif object_type == "pedestrian":
            if distance in ["close", "medium"]:
                return {"action": "slow_down_vehicle", "reason": "Pedestrian detected"}
            else:
                return {"action": "no_action", "reason": "Pedestrian far away"}
        elif object_type == "green light":
            return {"action": "speed_up_vehicle", "reason": "Green light ahead"}
        else:
            return {
                "action": "no_action",
                "reason": f"No specific action for {object_type}",
            }

    # Handle audio perceptions such as detecting sounds and their distances
    def handle_audio_perception(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Determine the sound type and distance to decide on an action
        sound = data.get("sound")
        distance = data.get("distance")

        if sound == "siren":
            if distance == "close":
                return {
                    "action": "change_lane",
                    "reason": "Emergency vehicle approaching",
                }
            else:
                return {
                    "action": "slow_down_vehicle",
                    "reason": "Potential emergency vehicle",
                }
        elif sound == "horn":
            return {"action": "slow_down_vehicle", "reason": "Vehicle honking nearby"}
        else:
            return {"action": "no_action", "reason": f"No specific action for {sound}"}

    # Handle traffic perceptions such as detecting traffic conditions
    def handle_traffic_perception(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Determine the traffic condition to decide on an action
        condition = data.get("condition")

        if condition == "clear":
            return {"action": "speed_up_vehicle", "reason": "Clear traffic conditions"}
        elif condition == "congested":
            return {"action": "slow_down_vehicle", "reason": "Traffic congestion ahead"}
        elif condition == "accident_ahead":
            return {"action": "change_lane", "reason": "Accident reported ahead"}
        else:
            return {
                "action": "no_action",
                "reason": f"No specific action for {condition}",
            }


# Main function to run the autonomous vehicle example
async def main():
    # Initialize the Frame and Framer configuration
    frame = Frame(
        openai_api_key=os.getenv("OPENAI_API_KEY", ""),
        mistral_api_key=os.getenv("MISTRAL_API_KEY", ""),
        huggingface_api_key=os.getenv("HUGGINGFACE_API_KEY", "")
    )
    config = FramerConfig(name="AutonomousVehicleFramer")
    framer = await frame.framer_factory.create_framer(config, plugins=frame.plugins)

    # Start driving when the script is run by finding the vehicle plugin
    vehicle_plugin = next(
        (
            plugin
            for plugin in framer.plugins.values()
            if isinstance(plugin, AutonomousVehiclePlugin)
        ),
        None,
    )
    if vehicle_plugin:
        await vehicle_plugin.start_driving()
        logger.info("Vehicle started driving automatically.")
    else:
        logger.warning("AutonomousVehiclePlugin not found. Vehicle not started.")

    # Set the execution context with the LLM service from the framer
    execution_context = ExecutionContext(llm_service=framer.llm_service)
    action_registry = ActionRegistry(execution_context=execution_context)

    # For this example demo, we will show how you can create an entirely new and custom action registry
    # in a plugin, and register it within a Framer to completely replace its behavior (not just default behavior)
    # but its behavior in other plugins.

    # By default plugins are loaded alphabetically, but you can specify which plugins to load first / last and in
    # what order to have greater control.

    # This is how you can do a custom action registry replacement to clear default actions
    action_registry.actions = {}
    action_registry.valid_actions = []

    # Set it to the same LLM service the Framer is using
    execution_context = ExecutionContext(llm_service=framer.llm_service)
    # Set the execution context's registry to the new action registry
    execution_context.action_registry = action_registry
    # Set the execution context agency to the framer's agency
    execution_context.agency = framer.agency

    vehicle_plugin = AutonomousVehiclePlugin(framer)
    process_perception_action = ProcessPerceptionAction(action_registry)

    # Register our actions in the new registry
    action_registry.add_action(StopVehicleAction(vehicle_plugin))
    action_registry.add_action(SlowDownVehicleAction(vehicle_plugin))
    action_registry.add_action(SpeedUpVehicleAction(vehicle_plugin))
    action_registry.add_action(ChangeLaneAction(vehicle_plugin))
    action_registry.add_action(StartDrivingAction(vehicle_plugin))
    action_registry.add_action(NoActionAction(vehicle_plugin))
    action_registry.add_action(BrakeVehicleAction(vehicle_plugin))
    action_registry.add_action(process_perception_action)

    # Replace the default action registry with the custom one defined above
    framer.brain.action_registry = action_registry
    # This is how you can do a custom action registry replacement
    # framer.brain.action_registry = action_registry
    # Set the execution context
    framer.execution_context = execution_context
    # This is how you can do a custom action registry replacement
    # framer.execution_context = execution_context

    # Define a list of perceptions to simulate the vehicle's environment
    perceptions = [
        # Each perception includes a type, data, and source
        {
            "type": "visual",
            "data": {"object": "start", "distance": "close"},
            "source": "camera",
        },
        {
            "type": "visual",
            "data": {"object": "green light", "distance": "medium"},
            "source": "camera",
        },
        {
            "type": "traffic",
            "data": {"condition": "clear"},
            "source": "traffic_system",
        },
        {
            "type": "visual",
            "data": {"object": "pedestrian", "distance": "close"},
            "source": "camera",
        },
        {
            "type": "audio",
            "data": {"sound": "siren", "distance": "far"},
            "source": "microphone",
        },
        {
            "type": "traffic",
            "data": {"condition": "accident_ahead"},
            "source": "traffic_system",
        },
        {
            "type": "visual",
            "data": {"object": "stop sign", "distance": "close"},
            "source": "camera",
        },
    ]

    # Process each perception in the list
    for perception in perceptions:
        # Log the perception being processed
        logger.info(f"Processing perception: {perception}")
        result = await action_registry.execute_action(
            "process_perception",
            perception=perception,
        )
        logger.info(f"Action result: {result}")
        await asyncio.sleep(1)

    # Close the Framer instance after processing all perceptions
    await framer.close()


if __name__ == "__main__":
    asyncio.run(main())
