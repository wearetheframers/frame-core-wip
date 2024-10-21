import asyncio
import time
from frame.src.framer.brain.plugins.base import BasePlugin
from frame.src.services.execution_context import ExecutionContext
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

    async def execute(self, action: str, params: Dict[str, Any]) -> str:
        if action == "stop_vehicle":
            return await self.stop_vehicle()
        elif action == "slow_down_vehicle":
            return await self.slow_down_vehicle()
        elif action == "speed_up_vehicle":
            return await self.speed_up_vehicle()
        elif action == "change_lane":
            return await self.change_lane()
        elif action == "start_driving":
            return await self.start_driving()
        elif action == "no_action":
            return await self.no_action()
        elif action == "brake_vehicle":
            return await self.brake_vehicle()
        else:
            raise ValueError(f"Unknown action: {action}")

    async def stop_vehicle(self) -> str:
        self.speed = 0
        self.is_driving = False
        return f"Vehicle stopped. Speed: {self.speed} km/h, Lane: {self.lane}"

    async def slow_down_vehicle(self) -> str:
        self.speed = max(0, self.speed - 10)
        return f"Vehicle slowing down. Speed: {self.speed} km/h, Lane: {self.lane}"

    async def speed_up_vehicle(self) -> str:
        self.speed = min(self.max_speed, self.speed + 10)
        return f"Vehicle speeding up. Speed: {self.speed} km/h, Lane: {self.lane}"

    async def change_lane(self) -> str:
        self.lane = 3 - self.lane  # Toggle between lane 1 and 2
        return f"Vehicle changing to lane {self.lane}. Speed: {self.speed} km/h"

    async def start_driving(self) -> str:
        self.is_driving = True
        self.speed = 60  # Start at 60 km/h
        return f"Vehicle started driving. Speed: {self.speed} km/h, Lane: {self.lane}"

    async def no_action(self) -> str:
        if self.is_driving:
            self.update_speed()
        return f"Vehicle continuing current action. Speed: {self.speed:.2f} km/h, Lane: {self.lane}"

    async def brake_vehicle(self) -> str:
        self.speed = max(0, self.speed - 20)
        return f"Vehicle braking. Speed: {self.speed} km/h, Lane: {self.lane}"


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
        return result


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
        return result


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
