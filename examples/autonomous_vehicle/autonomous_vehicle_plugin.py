import asyncio
from frame.src.framer.brain.plugins.base import BasePlugin
from frame.src.services.execution_context import ExecutionContext
from frame.src.framer.agency.priority import Priority
from typing import Dict, Any
from frame.src.framer.agency.actions import BaseAction


class AutonomousVehiclePlugin(BasePlugin):

    async def on_load(self):
        self.add_action("stop_vehicle", self.stop_vehicle, "Stop the autonomous vehicle")
        self.add_action("slow_down_vehicle", self.slow_down_vehicle, "Slow down the autonomous vehicle")
        self.add_action("change_lane", self.change_lane, "Change the lane of the autonomous vehicle")

    async def execute(self, action: str, params: Dict[str, Any]) -> str:
        if action == "stop_vehicle":
            return await self.stop_vehicle()
        elif action == "slow_down_vehicle":
            return await self.slow_down_vehicle()
        elif action == "change_lane":
            return await self.change_lane()
        else:
            raise ValueError(f"Unknown action: {action}")

    async def stop_vehicle(self) -> str:
        self.speed = 0
        return "Vehicle stopped"

    async def slow_down_vehicle(self) -> str:
        self.speed = max(0, self.speed - 10)
        return f"Vehicle slowing down. Current speed: {self.speed}"

    async def change_lane(self) -> str:
        self.lane = 3 - self.lane  # Toggle between lane 1 and 2
        return f"Vehicle changing to lane {self.lane}"


class StopVehicleAction(BaseAction):
    def __init__(self, vehicle_plugin: AutonomousVehiclePlugin):
        super().__init__(
            "stop_vehicle",
            "Stop the autonomous vehicle",
            Priority.HIGH,
        )
        self.vehicle_plugin = vehicle_plugin

    async def execute(self, execution_context: ExecutionContext, **kwargs) -> str:
        result = self.vehicle_plugin.stop_vehicle()
        print(f"{execution_context.config.name}: {result}")
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
        result = self.vehicle_plugin.slow_down_vehicle()
        print(f"{execution_context.config.name}: {result}")
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
        result = self.vehicle_plugin.change_lane()
        print(f"{execution_context.config.name}: {result}")
        await asyncio.sleep(0.1)
        return result
