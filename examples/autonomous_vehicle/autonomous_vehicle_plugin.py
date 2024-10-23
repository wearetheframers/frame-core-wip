import asyncio
import time
from frame.src.framer.brain.plugins.base import BasePlugin
from frame.src.services import ExecutionContext
from frame.src.framer.agency.priority import Priority
from typing import Dict, Any
from frame.src.framer.brain.actions import BaseAction


class AutonomousVehiclePlugin(BasePlugin):
    def __init__(self, framer):
        super().__init__(framer)
        self.speed = 0
        self.lane = 1
        self.is_driving = False
        self.max_speed = 120  # km/h
        self.acceleration = 5  # km/h per second
        self.last_update_time = time.time()  # Add this line to track time

    def update_speed(self):
        # Update speed based on time elapsed since last update
        current_time = time.time()
        elapsed_time = current_time - self.last_update_time
        if self.is_driving and self.speed < self.max_speed:
            self.speed = min(
                self.max_speed, self.speed + self.acceleration * elapsed_time
            )
        self.last_update_time = current_time

    async def on_load(self):
        # Register actions with the Framer's action registry
        # This is how you can normally call the plugin
        # self.add_action("stop_vehicle", self.stop_vehicle, "Stop the autonomous vehicle")
        # self.add_action("slow_down_vehicle", self.slow_down_vehicle, "Slow down the autonomous vehicle")
        # self.add_action("speed_up_vehicle", self.speed_up_vehicle, "Speed up the autonomous vehicle")
        # self.add_action("change_lane", self.change_lane, "Change the lane of the autonomous vehicle")
        # self.add_action("start_driving", self.start_driving, "Start driving the autonomous vehicle")
        # self.add_action("no_action", self.no_action, "Continue with the current action")
        # self.add_action("brake_vehicle", self.brake_vehicle, "Apply brakes to the vehicle")
        self.add_action(
            "stop_vehicle", self.stop_vehicle, "Stop the autonomous vehicle"
        )
        self.add_action(
            "slow_down_vehicle",
            self.slow_down_vehicle,
            "Slow down the autonomous vehicle",
        )
        self.add_action(
            "speed_up_vehicle",
            self.speed_up_vehicle,
            "Speed up the autonomous vehicle",
        )
        self.add_action(
            "change_lane", self.change_lane, "Change the lane of the autonomous vehicle"
        )
        self.add_action(
            "start_driving", self.start_driving, "Start driving the autonomous vehicle"
        )
        self.add_action("no_action", self.no_action, "Continue with the current action")
        self.add_action(
            "brake_vehicle", self.brake_vehicle, "Apply brakes to the vehicle"
        )

    async def execute(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        action_methods = {
            "stop_vehicle": self.stop_vehicle,
            "slow_down_vehicle": self.slow_down_vehicle,
            "speed_up_vehicle": self.speed_up_vehicle,
            "change_lane": self.change_lane,
            "start_driving": self.start_driving,
            "no_action": self.no_action,
            "brake_vehicle": self.brake_vehicle,
        }

        if action in action_methods:
            result = await action_methods[action]()
            result = {
                "response": result,
                "reasoning": f"Executed action '{action}' with parameters {params}.",
                "confidence": 0.9,
                "priority": 1,
                "task_status": "COMPLETED",
                "related_roles": [],
                "related_goals": [],
            }
        else:
            result = {
                "response": f"Unknown action: {action}",
                "reasoning": "No reasoning provided.",
                "confidence": 0.0,
                "priority": 1,
                "related_roles": [],
                "related_goals": [],
            }
        return result

    async def stop_vehicle(self) -> Dict[str, Any]:
        self.speed = 0
        self.is_driving = False
        return {"speed": self.speed, "lane": self.lane, "result": "Vehicle stopped"}

    async def slow_down_vehicle(self) -> Dict[str, Any]:
        self.speed = max(0, self.speed - 10)
        return {"speed": self.speed, "lane": self.lane, "result": "Vehicle slowing down"}

    async def speed_up_vehicle(self) -> Dict[str, Any]:
        self.speed = min(self.max_speed, self.speed + 10)
        return {"speed": self.speed, "lane": self.lane, "result": "Vehicle speeding up"}

    async def change_lane(self) -> Dict[str, Any]:
        self.lane = 3 - self.lane  # Toggle between lane 1 and 2
        return {"speed": self.speed, "lane": self.lane, "result": f"Vehicle changing to lane {self.lane}"}

    async def start_driving(self) -> Dict[str, Any]:
        self.is_driving = True
        self.speed = 60  # Start at 60 km/h
        return {"speed": self.speed, "lane": self.lane, "result": "Vehicle started driving"}

    async def no_action(self) -> Dict[str, Any]:
        if self.is_driving:
            self.update_speed()
        return {"speed": self.speed, "lane": self.lane, "result": "Vehicle continuing current action"}

    async def brake_vehicle(self) -> Dict[str, Any]:
        self.speed = max(0, self.speed - 20)
        return {"speed": self.speed, "lane": self.lane, "result": "Vehicle braking"}


class StopVehicleAction(BaseAction):
    def __init__(self, vehicle_plugin: AutonomousVehiclePlugin):
        super().__init__(
            "stop_vehicle",
            "Stop the autonomous vehicle",
            Priority.HIGH,
        )
        self.vehicle_plugin = vehicle_plugin

    async def execute(self, execution_context: ExecutionContext, **kwargs) -> str:
        result = await self.vehicle_plugin.stop_vehicle()
        print(f"Vehicle: {result}")
        await asyncio.sleep(0.1)
        return {"response": result}


class SlowDownVehicleAction(BaseAction):
    def __init__(self, vehicle_plugin: AutonomousVehiclePlugin):
        super().__init__(
            "slow_down_vehicle",
            "Slow down the autonomous vehicle",
            Priority.MEDIUM,
        )
        self.vehicle_plugin = vehicle_plugin

    async def execute(self, execution_context: ExecutionContext, **kwargs) -> str:
        result = await self.vehicle_plugin.slow_down_vehicle()
        print(f"Vehicle: {result}")
        await asyncio.sleep(0.1)
        return {"response": result}


class SpeedUpVehicleAction(BaseAction):
    def __init__(self, vehicle_plugin: AutonomousVehiclePlugin):
        super().__init__(
            "speed_up_vehicle",
            "Speed up the autonomous vehicle",
            Priority.MEDIUM,
        )
        self.vehicle_plugin = vehicle_plugin

    async def execute(self, execution_context: ExecutionContext, **kwargs) -> str:
        result = await self.vehicle_plugin.speed_up_vehicle()
        print(f"Vehicle: {result}")
        await asyncio.sleep(0.1)
        return result


class ChangeLaneAction(BaseAction):
    def __init__(self, vehicle_plugin: AutonomousVehiclePlugin):
        super().__init__(
            "change_lane",
            "Change the lane of the autonomous vehicle",
            Priority.LOW,
        )
        self.vehicle_plugin = vehicle_plugin

    async def execute(self, execution_context: ExecutionContext, **kwargs) -> str:
        result = await self.vehicle_plugin.change_lane()
        print(f"Vehicle: {result}")
        await asyncio.sleep(0.1)
        return result


class StartDrivingAction(BaseAction):
    def __init__(self, vehicle_plugin: AutonomousVehiclePlugin):
        super().__init__(
            "start_driving",
            "Start driving the autonomous vehicle",
            Priority.HIGH,
        )
        self.vehicle_plugin = vehicle_plugin

    async def execute(self, execution_context: ExecutionContext, **kwargs) -> str:
        result = await self.vehicle_plugin.start_driving()
        print(f"Vehicle: {result}")
        await asyncio.sleep(0.1)
        return result


class NoActionAction(BaseAction):
    def __init__(self, vehicle_plugin: AutonomousVehiclePlugin):
        super().__init__(
            "no_action",
            "Continue with the current action",
            Priority.LOW,
        )
        self.vehicle_plugin = vehicle_plugin

    async def execute(self, execution_context: ExecutionContext, **kwargs) -> str:
        result = await self.vehicle_plugin.no_action()
        print(f"Vehicle: {result}")
        await asyncio.sleep(0.1)
        return result


class BrakeVehicleAction(BaseAction):
    def __init__(self, vehicle_plugin: AutonomousVehiclePlugin):
        super().__init__(
            "brake_vehicle",
            "Apply brakes to the vehicle",
            Priority.HIGH,
        )
        self.vehicle_plugin = vehicle_plugin

    async def execute(self, execution_context: ExecutionContext, **kwargs) -> str:
        result = await self.vehicle_plugin.brake_vehicle()
        print(f"Vehicle: {result}")
        await asyncio.sleep(0.1)
        return result
