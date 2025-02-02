import asyncio
import logging
import time
from frame.frame import Frame
from frame.src.framer import Framer
from typing import Dict, Any, List, Optional

from frame.src.framer.config import FramerConfig
from frame.src.services.llm import LLMService
from frame.src.framer.framer_factory import FramerFactory

logger = logging.getLogger(__name__)


class SyncFrame:
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service

    def create_framer(self, config: FramerConfig) -> Framer:
        """
        Create a Framer instance synchronously.

        Args:
            config (FramerConfig): Configuration for the Framer.

        Returns:
            Framer: A new Framer instance.
        """
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(
            FramerFactory(config, self.llm_service).create_framer()
        )

    def perform_task(self, framer: Framer, task: dict) -> dict:
        """
        Perform a task synchronously.

        Args:
            framer (Framer): The Framer instance.
            task (dict): The task details.

        Returns:
            dict: The result of the task execution.
        """
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(framer.perform_task(task))

    def process_perception(self, framer: Framer, perception: dict) -> dict:
        """
        Process a perception synchronously.

        Args:
            framer (Framer): The Framer instance.
            perception (dict): The perception details.

        Returns:
            dict: The decision made based on the perception.
        """
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(framer.sense(perception))

    def generate_tasks_from_perception(
        self, framer: Framer, perception: dict, max_len: int = None
    ) -> list:
        """
        Generate tasks from a perception synchronously.

        Args:
            framer (Framer): The Framer instance.
            perception (dict): The perception details.
            max_len (int, optional): Maximum number of tasks to generate.

        Returns:
            list: A list of generated tasks.
        """
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(
            framer.generate_tasks_from_perception(perception, max_len)
        )

    def close_framer(self, framer: Framer) -> None:
        """
        Close the Framer instance synchronously.

        Args:
            framer (Framer): The Framer instance to close.
        """
        loop = asyncio.get_event_loop()
        loop.run_until_complete(framer.close())
