from typing import Any, Dict, Optional, Callable
from frame.src.services.llm.main import LLMService
from frame.src.services.memory.main import MemoryService
from frame.src.services.eq.main import EQService
from frame.src.framer.soul.soul import Soul
from frame.src.framer.config import FramerConfig
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from frame.src.framer.agency.agency import Agency


class ExecutionContext:
    """
    ExecutionContext provides a centralized container for various services, state, and functions
    that actions and components might need during execution. It ensures consistent access to resources
    across all actions and facilitates easier testing, modular design, and state management.

    The ExecutionContext serves as a bridge between different components of the Framer,
    allowing them to share resources and functionality without tight coupling.

    Key features:
    - Centralized service access: Provides access to core services like LLM, memory, and EQ.
    - State management: Maintains a dictionary for storing and retrieving arbitrary state information.
    - Function delegation: Holds references to key functions from other components for easy access.
    - Configuration access: Stores the Framer configuration for global access.
    - Framer reference: Maintains a reference to the parent Framer instance.

    Attributes:
        llm_service (LLMService): The language model service for text generation and processing.
        memory_service (Optional[MemoryService]): The memory service for storing and retrieving information.
        eq_service (Optional[EQService]): The emotional intelligence service for EQ-related functionality.
        soul (Optional[Soul]): The soul component of the Framer, representing its core essence and personality.
        state (Dict[str, Any]): A dictionary to store any additional state information.
        process_perception (Optional[Callable]): A function to process perceptions.
        execute_decision (Optional[Callable]): A function to execute decisions.
        config (Optional[FramerConfig]): The configuration for the Framer.
        perform_task (Optional[Callable]): A function to perform tasks, typically bound from Agency.
        agency (Optional[Agency]): The agency component of the Framer.
        framer (Optional[Framer]): The parent Framer instance.

    The ExecutionContext class plays a crucial role in maintaining a clean and modular architecture
    within the Framer system, promoting loose coupling and easier testing of individual components.
    """

    def __init__(
        self,
        llm_service: LLMService,
        memory_service: Optional[MemoryService] = None,
        eq_service: Optional[EQService] = None,
        perform_task: Optional[Callable] = None,
        soul: Optional[Soul] = None,
        state: Optional[Dict[str, Any]] = None,
        process_perception: Optional[Callable] = None,
        execute_decision: Optional[Callable] = None,
        config: Optional[FramerConfig] = None,
        agency: Optional["Agency"] = None,
    ):
        self.llm_service = llm_service
        self.memory_service = memory_service
        self.eq_service = eq_service
        self.perform_task = perform_task
        self.soul = soul
        self.state = state or {}
        self.process_perception = process_perception
        self.execute_decision = execute_decision
        self.config = config
        self.agency = agency

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

    async def perform_task_wrapper(self, *args, **kwargs):
        if self.perform_task:
            return await self.perform_task(*args, **kwargs)
        raise NotImplementedError("perform_task method not set")

    def set_goals(self, goals):
        if self.agency:
            self.agency.set_goals(goals)
        else:
            raise AttributeError("Agency is not set in ExecutionContext")

    def set_roles(self, roles):
        if self.agency:
            self.agency.set_roles(roles)
        else:
            raise AttributeError("Agency is not set in ExecutionContext")
