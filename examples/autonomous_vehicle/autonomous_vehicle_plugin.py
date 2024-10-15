import asyncio


class AutonomousVehiclePlugin:

    def __init__(self):
        # Initialize any necessary state or resources
        pass

    async def stop_vehicle(self, framer):
        print(f"{framer.config.name}: Vehicle stopped")
        await asyncio.sleep(0.1)

    async def slow_down_vehicle(self, framer):
        print(f"{framer.config.name}: Vehicle slowing down")
        await asyncio.sleep(0.1)

    async def change_lane(self, framer):
        print(f"{framer.config.name}: Vehicle changing lane")
        await asyncio.sleep(0.1)
