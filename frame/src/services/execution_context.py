from typing import Any, Dict, Optional, Callable
from frame.src.services.llm.main import LLMService
from frame.src.services.memory.main import MemoryService
from frame.src.services.eq.main import EQService
from frame.src.framer.soul.soul import Soul
from frame.src.framer.config import FramerConfig


class ExecutionContext:
    """
    ExecutionContext provides a centralized container for various services and state
    that actions might need during execution. It ensures consistent access to resources
    across all actions and facilitates easier testing and modular design.

    Attributes:
        llm_service (LLMService): The language model service.
        memory_service (MemoryService): The memory service for storing and retrieving information.
        eq_service (EQService): The emotional intelligence service.
        soul (Soul): The soul component of the Framer.
        state (Dict[str, Any]): A dictionary to store any additional state information.
        process_perception (Callable): A function to process perceptions.
        execute_decision (Callable): A function to execute decisions.
        config (FramerConfig): The configuration for the Framer.
    """

    def __init__(
        self,
        llm_service: LLMService,
        memory_service: Optional[MemoryService] = None,
        eq_service: Optional[EQService] = None,
        soul: Optional[Soul] = None,
        state: Optional[Dict[str, Any]] = None,
        process_perception: Optional[Callable] = None,
        execute_decision: Optional[Callable] = None,
        config: Optional[FramerConfig] = None,
    ):
        self.llm_service = llm_service
        self.memory_service = memory_service
        self.eq_service = eq_service
        self.soul = soul
        self.state = state or {}
        self.process_perception = process_perception
        self.execute_decision = execute_decision
        self.config = config

    def update_state(self, key, value):
        self.state[key] = value

    def get_state(self, key):
        return self.state.get(key)

    def set_framer(self, framer):
        self.framer = framer

    def get_framer(self):
        return self.framer

    async def process_perception_wrapper(self, *args, **kwargs):
        if self.process_perception:
            return await self.process_perception(*args, **kwargs)
        raise NotImplementedError("process_perception method not set")

    async def execute_decision_wrapper(self, *args, **kwargs):
        if self.execute_decision:
            return await self.execute_decision(*args, **kwargs)
        raise NotImplementedError("execute_decision method not set")
