import logging
from typing import Dict, Any
from frame.src.framer.brain.plugins.base import BasePlugin


class MoodLightingPlugin(BasePlugin):
    def __init__(self, framer=None):
        super().__init__(framer)
        self.logger = logging.getLogger(self.__class__.__name__)

    async def on_load(self, framer):
        self.framer = framer
        self.logger.info("MoodLightingPlugin loaded")
        self.register_actions(framer.brain.action_registry)

    def register_actions(self, action_registry):
        self.add_action(
            name="adjust_lighting",
            action_func=self.adjust_lighting,
            description="Adjust the lighting based on the Framer's emotional state",
        )

    async def adjust_lighting(self, execution_context: Any, mood: str) -> str:
        # Simulate adjusting lighting based on mood
        self.logger.info(f"Adjusting lighting for mood: {mood}")
        if mood == "happy":
            return "Setting lights to bright and warm."
        elif mood == "calm":
            return "Setting lights to dim and cool."
        elif mood == "focused":
            return "Setting lights to bright and neutral."
        else:
            return "Setting lights to default settings."

    async def on_remove(self):
        self.logger.info("MoodLightingPlugin removed")

    async def execute(self, action: str, params: Dict[str, Any]) -> Any:
        if action == "adjust_lighting":
            mood = params.get("mood", "neutral")
            return await self.adjust_lighting(self.execution_context, mood)
        else:
            raise ValueError(f"Unknown action: {action}")
