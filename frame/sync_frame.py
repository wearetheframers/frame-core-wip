import asyncio
import logging
import time
from frame.frame import Frame
from frame.src.framer import Framer
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)


class SyncFrame:
    """
    A synchronous wrapper for the asynchronous Frame class.

    This class provides a synchronous interface to the asynchronous operations
    of the Frame class, making it easier to use in synchronous contexts.
    """

    def __init__(self):
        """
        Initialize the SyncFrame with an asynchronous Frame and event loop.
        """
        self.async_frame = Frame()
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    async def create_framer(self, **kwargs: Any) -> "Framer":
        """
        Create a new Framer instance.

        Args:
            **kwargs: Keyword arguments to pass to the Frame.create_framer method.

        Returns:
            The created Framer instance.
        """
        return await self.async_frame.create_framer(**kwargs)

    async def perform_task(self, framer: Any, task: Dict[str, Any]) -> Any:
        """
        Perform a task using the given Framer.

        Args:
            framer: The Framer instance to use.
            task: The task to perform.

        Returns:
            The result of the task.
        """
        return await framer.perform_task(task)

    def generate_tasks_from_perception(
        self,
        framer: Any,
        perception: Dict[str, Any],
        max_len: int = 2048,
        timeout: int = 30,
    ) -> List[Dict[str, Any]]:
        """
        Generate tasks from a given perception.

        Args:
            framer: The Framer instance to use.
            perception: The perception to generate tasks from.
            max_len: The maximum length of the generated tasks.
            timeout: The maximum time to wait for task generation.

        Returns:
            A list of generated tasks or an empty list if timeout occurs.
        """
        logger.info(f"Starting generate_tasks_from_perception with timeout {timeout}")
        start_time = time.time()
        try:
            logger.debug("Calling generate_tasks_from_perception coroutine")
            result = self.run_async(
                asyncio.wait_for(
                    framer.generate_tasks_from_perception(perception, max_len=max_len),
                    timeout=timeout,
                )
            )
            logger.debug("generate_tasks_from_perception coroutine completed")
            logger.info(
                f"Task generation completed in {time.time() - start_time:.2f} seconds"
            )
            return result
        except asyncio.TimeoutError:
            logger.error(
                f"Task generation timed out after {time.time() - start_time:.2f} seconds"
            )
            return []
        except Exception as e:
            logger.error(f"Error in generate_tasks_from_perception: {str(e)}")
            return []

    async def sense(self, framer: Any, perceptions: List[Dict[str, Any]]) -> Any:
        """
        Process perceptions using the given Framer.

        Args:
            framer: The Framer instance to use.
            perceptions: The perceptions to process.

        Returns:
            The result of processing the perceptions.
        """
        return await framer.sense(perceptions)

    def process_perception(self, framer: Any, perception: Dict[str, Any]) -> Any:
        """
        Synchronously process perceptions using the given Framer.

        Args:
            framer: The Framer instance to use.
            perception: The perception to process.

        Returns:
            The result of processing the perception.
        """
        return self.run_async(framer.sense(perception))

    def run_async(self, coroutine: asyncio.Future) -> Any:
        """
        Run an asynchronous coroutine in the synchronous context.

        Args:
            coroutine: The asynchronous coroutine to run.

        Returns:
            The result of the coroutine.
        """
        logger.info("Starting run_async")
        start_time = time.time()
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                logger.info("Loop is already running, using run_coroutine_threadsafe")
                result = asyncio.run_coroutine_threadsafe(coroutine, loop).result()
            else:
                logger.info("Loop is not running, using run_until_complete")
                result = loop.run_until_complete(
                    asyncio.wait_for(coroutine, timeout=60)
                )
            logger.info(
                f"run_async completed in {time.time() - start_time:.2f} seconds"
            )
            return result
        except RuntimeError:
            logger.warning("RuntimeError occurred, creating new event loop")
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(coroutine)
            logger.info(
                f"run_async completed in {time.time() - start_time:.2f} seconds"
            )
            return result
        except Exception as e:
            logger.error(f"Error in run_async: {str(e)}")
            raise

    def close(self):
        """
        Close the event loop associated with this SyncFrame.
        """
        self.loop.close()

    # Add more synchronous wrapper methods as needed


sync_frame = SyncFrame()
import asyncio
from frame.src.framer.framer import Framer
from frame.src.framer.config import FramerConfig
from frame.src.services.llm.main import LLMService
from frame.src.framer.framer_factory import FramerFactory


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
