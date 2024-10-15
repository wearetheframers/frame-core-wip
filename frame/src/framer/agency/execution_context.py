from typing import Optional, Dict, Any
from frame.src.services.llm.main import LLMService
from frame.src.services.memory.main import MemoryService
from frame.src.services.eq.main import EQService
from frame.src.framer.soul.soul import Soul

__all__ = ["ExecutionContext"]


class ExecutionContext:
    def __init__(
        self,
        llm_service: LLMService,
        memory_service: Optional[MemoryService] = None,
        eq_service: Optional[EQService] = None,
        soul: Optional[Soul] = None,
        state: Dict[str, Any] = None,
    ):
        self.llm_service = llm_service
        self.memory_service = memory_service
        self.eq_service = eq_service
        self.soul = soul
        self.state = state or {}

    def set_state(self, key: str, value: Any) -> None:
        self.state[key] = value

    def get_state(self, key: str, default: Any = None) -> Any:
        return self.state.get(key, default)
