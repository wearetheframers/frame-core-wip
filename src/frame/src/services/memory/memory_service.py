from typing import Dict, Any, List, Optional
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from frame.src.framer.brain.memory.memory_adapter_interface import (
        MemoryAdapterInterface,
    )


class MemoryService:
    def __init__(self, adapter: "MemoryAdapterInterface"):
        self.adapter = adapter

    def add_memory(
        self, memory: str, user_id: str = "default", metadata: Dict[str, Any] = None
    ) -> int:
        return self.adapter.add(memory, user_id, metadata)

    def retrieve_memory(
        self, memory_id: int, user_id: str = "default"
    ) -> Optional[Any]:
        return self.adapter.retrieve(memory_id, user_id)

    def update_memory(
        self, memory_id: int, data: str, user_id: str = "default"
    ) -> bool:
        return self.adapter.update(memory_id, data, user_id)

    def delete_memory(self, memory_id: int, user_id: str = "default") -> bool:
        return self.adapter.delete(memory_id, user_id)

    def get_all_memories(self, user_id: str = "default") -> List[Dict[str, Any]]:
        return self.adapter.get_all(user_id)

    def search_memories(
        self, query: str, user_id: str = "default"
    ) -> List[Dict[str, Any]]:
        return self.adapter.search(query, user_id)

    def get_memory_history(self, memory_id: int, user_id: str = "default") -> List[str]:
        return self.adapter.history(memory_id, user_id)

    def clear_all_memories(self, user_id: str = "default") -> bool:
        return self.adapter.clear_all(user_id)

    def get_memory_count(self, user_id: str = "default") -> int:
        return self.adapter.get_count(user_id)
