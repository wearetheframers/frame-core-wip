import asyncio


class AutonomousVehiclePlugin:

    def __init__(self):
        # Initialize any necessary state or resources
        self.speed = 0
        self.lane = 1

    async def stop_vehicle(self, execution_context):
        self.speed = 0
        print(f"{execution_context.framer.config.name}: Vehicle stopped")
        await asyncio.sleep(0.1)

    async def slow_down_vehicle(self, execution_context):
        self.speed = max(0, self.speed - 10)
        print(
            f"{execution_context.framer.config.name}: Vehicle slowing down. Current speed: {self.speed}"
        )
        await asyncio.sleep(0.1)

    async def change_lane(self, execution_context):
        self.lane = 3 - self.lane  # Toggle between lane 1 and 2
        print(
            f"{execution_context.framer.config.name}: Vehicle changing to lane {self.lane}"
        )
        await asyncio.sleep(0.1)
