from typing import Dict, Any, List, Optional


class MemoryService:
    def __init__(self, adapter):
        self.adapter = adapter

    def add_memory(
        self, memory: str, user_id: str = "default", metadata: Dict[str, Any] = None
    ):
        self.adapter.add(memory, user_id, metadata)

    def get_all_memories(self, user_id: str = "default") -> List[Dict[str, Any]]:
        return self.adapter.get_all(user_id)

    def search_memories(
        self, query: str, user_id: str = "default"
    ) -> List[Dict[str, Any]]:
        return self.adapter.search(query, user_id)

    def update_memory(self, memory_id: int, data: str, user_id: str = "default"):
        self.adapter.update(memory_id, data, user_id)

    def get_memory_history(self, memory_id: int, user_id: str = "default") -> List[str]:
        return self.adapter.history(memory_id, user_id)
