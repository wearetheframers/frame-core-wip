# Autonomous Vehicle Example

This example demonstrates how to use the Frame framework to create a simple autonomous vehicle system. The system processes various perceptions and makes decisions based on them.

## Code Structure

The example consists of two main files:

1. `main.py`: This file sets up the Frame, initializes the necessary components, and simulates the perception processing.
2. `autonomous_vehicle_plugin.py`: This file contains the plugin with actions that the autonomous vehicle can take.

## Main Script (main.py)

```python
import sys
import os
import asyncio

# Add the frame-core directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from frame.frame import Frame
from frame.src.framer.config import FramerConfig
from frame.src.services.llm.main import LLMService
from frame.src.framer.framer_factory import FramerFactory
from frame.src.framer.agency.tasks.workflow.workflow_manager import WorkflowManager
from autonomous_vehicle_plugin import AutonomousVehiclePlugin

async def main():
    # Initialize the Frame
    frame = Frame()

    # Initialize services and components
    llm_service = LLMService()
    config = FramerConfig(name="AutonomousVehicleFramer")

    roles = ["Driver"]
    goals = ["Navigate safely"]
    
    framer_factory = FramerFactory(config, llm_service)
    framer = await framer_factory.create_framer(
        soul_seed="Autonomous Vehicle Soul",
        memory_service=None,
        eq_service=None
    )
    
    framer.set_roles(roles)
    framer.set_goals(goals)

    # Initialize and register the plugin
    av_plugin = AutonomousVehiclePlugin()
    framer.brain.action_registry.register_action("stop", av_plugin.stop_vehicle)
    framer.brain.action_registry.register_action("slow_down", av_plugin.slow_down_vehicle)
    framer.brain.action_registry.register_action("change_lane", av_plugin.change_lane)

    # Simulate perceptions
    perceptions = [
        {"type": "visual", "data": {"object": "stop sign", "distance": "far"}, "source": "camera"},
        {"type": "visual", "data": {"object": "stop sign", "distance": "close"}, "source": "camera"},
        {"type": "visual", "data": {"object": "pedestrian", "distance": "medium"}, "source": "camera"},
        {"type": "audio", "data": {"sound": "siren", "distance": "far"}, "source": "microphone"},
        {"type": "audio", "data": {"sound": "siren", "distance": "close"}, "source": "microphone"}
    ]

    # Process perceptions and make decisions
    for perception in perceptions:
        print(f"\nProcessing perception: {perception}")
        decision = await framer.process_perception(perception)
        print(f"Decision made: {decision}")

        if decision:
            await framer.brain.execute_decision(decision)
            
        # Add a small delay to simulate time passing between perceptions
        await asyncio.sleep(1)

# Run the example
if __name__ == "__main__":
    asyncio.run(main())
```

## Autonomous Vehicle Plugin (autonomous_vehicle_plugin.py)

```python
class AutonomousVehiclePlugin:

    def __init__(self):
        # Initialize any necessary state or resources
        pass
    
    def stop_vehicle(self):
        print("Vehicle stopped")

    def slow_down_vehicle(self):
        print("Vehicle slowing down")

    def change_lane(self):
        print("Vehicle changing lane")

    def self_driving_action(self, *args, **kwargs):
        """
        Implement the self-driving action here.
        
        Args:
            *args: Positional arguments passed to the action.
            **kwargs: Keyword arguments passed to the action.
        
        Returns:
            str: The result of the self-driving action.
        """
        # Your implementation here
        return "Self-driving action executed"

    def object_detection_action(self, *args, **kwargs):
        """
        Implement the object detection action here.
        
        Args:
            *args: Positional arguments passed to the action.
            **kwargs: Keyword arguments passed to the action.
        
        Returns:
            str: The result of the object detection action.
        """
        # Your implementation here
        return "Object detection action executed"
```

## Running the Example

To run this example, execute the `main.py` script:

```
python examples\autonomous_vehicle\main.py
```

## Example Output

Here's an example of what you might see when running the script:

```
Processing perception: {'type': 'visual', 'data': {'object': 'stop sign', 'distance': 'far'}, 'source': 'camera'}
Decision made: action='think' parameters={} expected_results=None reasoning='The perception of a far stop sign does not require an immediate action such as stopping the vehicle. It is important to process the information and consider the distance before deciding on any action.' confidence=0.8 priority=5 task_status=<TaskStatusModel.PENDING: 'pending'>

Processing perception: {'type': 'visual', 'data': {'object': 'stop sign', 'distance': 'close'}, 'source': 'camera'}
Decision made: action='stop' parameters={'object': 'stop sign', 'distance': 'close'} expected_results=None reasoning='A close stop sign requires an immediate action to ensure safe navigation.' confidence=0.9 priority=10 task_status=<TaskStatusModel.PENDING: 'pending'>
Vehicle stopped

Processing perception: {'type': 'visual', 'data': {'object': 'pedestrian', 'distance': 'medium'}, 'source': 'camera'}
Decision made: action='slow_down' parameters={'object': 'pedestrian', 'distance': 'medium'} expected_results=None reasoning="The perception of a pedestrian at a medium distance indicates a potential need to reduce the vehicle's speed to ensure safe navigation. It's important to be cautious and prepared to stop if necessary." confidence=0.8 priority=7 task_status=<TaskStatusModel.PENDING: 'pending'>
Vehicle slowing down

Processing perception: {'type': 'audio', 'data': {'sound': 'siren', 'distance': 'far'}, 'source': 'microphone'}
Decision made: action='think' parameters={} expected_results=None reasoning="The siren sound is far away, so there is no immediate danger. As a driver, it's important to stay alert and aware of the surroundings, but there is no urgent action required at this moment." confidence=0.8 priority=5 task_status=<TaskStatusModel.PENDING: 'pending'>

Processing perception: {'type': 'audio', 'data': {'sound': 'siren', 'distance': 'close'}, 'source': 'microphone'}
Decision made: action='change_lane' parameters={'lane': 'adjacent'} expected_results=None reasoning="The perception of a close siren indicates that emergency vehicles may be approaching, so it's safer to change lanes to make way for them." confidence=0.8 priority=9 task_status=<TaskStatusModel.PENDING: 'pending'>
Vehicle changing lane
```

This output shows how the autonomous vehicle system processes different perceptions and makes decisions based on them. The system thinks about far objects, stops for close stop signs, slows down for pedestrians, and changes lanes when emergency vehicles are approaching.
