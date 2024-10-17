from typing import Optional, Dict, Any
from frame.src.services.llm.main import LLMService
from frame.src.services.memory.main import MemoryService
from frame.src.services.eq.eq_service import EQService
from frame.src.framer.soul.soul import Soul


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

    def get_llm_service(self) -> LLMService:
        return self.llm_service

    def get_memory_service(self) -> Optional[MemoryService]:
        return self.memory_service

    def get_eq_service(self) -> Optional[EQService]:
        return self.eq_service

    def get_soul(self) -> Optional[Soul]:
        return self.soul

    def update_state(self, new_state: Dict[str, Any]) -> None:
        self.state.update(new_state)

    def get_full_state(self) -> Dict[str, Any]:
        return self.state.copy()
