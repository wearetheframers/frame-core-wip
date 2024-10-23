from __future__ import annotations
from typing import Optional, Dict, Any, List, TYPE_CHECKING, Union
from frame.src.services.llm.main import LLMService

if TYPE_CHECKING:
    from frame.src.services.llm.main import LLMService
    from frame.src.services.memory.main import MemoryService
    from frame.src.framer.config import FramerConfig
    from frame.src.services.eq.eq_service import EQService
    from frame.src.framer.soul.soul import Soul
    from frame.src.framer.brain.brain import Brain


class ExecutionContext:
    """
    ExecutionContext provides a centralized container for various services, state, and functions
    that actions and components might need during execution. It ensures consistent access to resources
    across all actions and facilitates easier testing, modular design, and state management.

    The ExecutionContext serves as a bridge between different components of the Framer,
    allowing them to share resources and functionality without tight coupling.

    Key features:
    - Centralized service access: Provides access to core services like LLM, memory, and EQ.
    - State management: Maintains and updates the current state of the execution.
    - Goal tracking: Manages the current goals of the Framer.
    - Action registry: Stores and manages available actions.
    """

    def __init__(
        self,
        llm_service: "LLMService",
        memory_service: Optional["MemoryService"] = None,
        eq_service: Optional["EQService"] = None,
        soul: Optional["Soul"] = None,
        brain: Optional["Brain"] = None,
        state: Dict[str, Any] = None,
        config: Optional[Union[FramerConfig, Dict[str, Any]]] = None,
    ):
        self.config = config
        self.llm_service = llm_service
        self.memory_service = memory_service
        self.eq_service = eq_service
        self.soul = soul
        self.brain = brain
        self.state = state or {}
        self.goals: List[Any] = []
        self.roles: List[Any] = []
        self.action_registry = None

    def set_roles(self, roles: List[Any]):
        self.roles = roles

    def set_goals(self, goals: List[Any]):
        self.goals = goals

    def set_state(self, key: str, value: Any) -> None:
        self.state[key] = value

    def get_state(self, key: Optional[str] = None, default: Any = None) -> Any:
        if key is None:
            return self.state
        return self.state.get(key, default)

    def get_llm_service(self) -> LLMService:
        return self.llm_service

    def get_memory_service(self) -> Optional[MemoryService]:
        return self.memory_service

    def get_eq_service(self) -> Optional[EQService]:
        return self.eq_service

    def get_soul(self) -> Optional[Soul]:
        return self.soul

    def get_brain(self) -> Optional["Brain"]:
        return self.brain

    def update_state(self, new_state: Dict[str, Any]) -> None:
        self.state.update(new_state)

    def get_full_state(self) -> Dict[str, Any]:
        return self.state.copy()

    def set_goals(self, goals: List[Any]):
        """
        Set the current goals for the Framer.

        Args:
            goals (List[Any]): A list of Goal objects to set as the current goals.
        """
        self.goals = goals

    def get_goals(self) -> List[Any]:
        """
        Get the current goals of the Framer.

        Returns:
            List[Any]: A list of the current Goal objects.
        """
        return self.goals

    def set_roles(self, roles: List[Any]):
        """
        Set the current roles for the Framer.

        Args:
            roles (List[Any]): A list of Role objects to set as the current roles.
        """
        self.roles = roles

    def get_roles(self) -> List[Any]:
        """
        Get the current roles of the Framer.

        Returns:
            List[Any]: A list of the current Role objects.
        """
        return self.roles

    async def generate_goals(self) -> List[Any]:
        """
        Generate new goals for the Framer.

        Returns:
            List[Any]: A list of newly generated Goal objects.
        """
        # This is a placeholder implementation. You should implement the actual goal generation logic here.
        # For now, we'll return an empty list.
        return []

    async def perform_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform a task using the LLM service.

        Args:
            task (Dict[str, Any]): A dictionary containing task details.

        Returns:
            Dict[str, Any]: The result of the task execution.
        """
        # This is a simple implementation. You might want to expand this based on your specific needs.
        prompt = f"Perform the following task: {task['description']}"
        response = await self.llm_service.get_completion(prompt)
        return {"output": response}

    async def generate_goals(self) -> List[Any]:
        """
        Generate new goals for the Framer.

        Returns:
            List[Any]: A list of newly generated Goal objects.
        """
        # This is a placeholder implementation. You should implement the actual goal generation logic here.
        # For now, we'll return an empty list.
        return []
