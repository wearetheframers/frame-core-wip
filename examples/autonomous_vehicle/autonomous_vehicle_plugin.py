import asyncio
from frame.src.framer.agency.actions import BaseAction
from frame.src.services.execution_context import ExecutionContext
from frame.src.framer.agency.priority import Priority


class AutonomousVehiclePlugin:

    def __init__(self):
        # Initialize any necessary state or resources
        self.speed = 0
        self.lane = 1

    def stop_vehicle(self):
        self.speed = 0
        return "Vehicle stopped"

    def slow_down_vehicle(self):
        self.speed = max(0, self.speed - 10)
        return f"Vehicle slowing down. Current speed: {self.speed}"

    def change_lane(self):
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
