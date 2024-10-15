from typing import Optional
from frame.src.services.llm.main import LLMService
from frame.src.services.memory.main import MemoryService
from frame.src.services.eq.main import EQService

class ExecutionContext:
    def __init__(
        self,
        llm_service: LLMService,
        memory_service: Optional[MemoryService] = None,
        eq_service: Optional[EQService] = None
    ):
        self.llm_service = llm_service
        self.memory_service = memory_service
        self.eq_service = eq_service
