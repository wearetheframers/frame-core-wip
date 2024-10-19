from typing import Dict, Any, List, Optional


from typing import Any, Dict, List, Optional

from frame.src.framer.brain.memory.memory_adapter_interface import (
    MemoryAdapterInterface,
)


class Mem0Adapter(MemoryAdapterInterface):
    """
    Adapter for basic memory operations.

    This class provides methods to interact with the memory storage,
    including adding, retrieving, and searching memories.
    """

    def __init__(self):
        self.storage = {}

    def store(
        self,
        memory: str,
        user_id: str = "default",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> int:
        if user_id not in self.storage:
            self.storage[user_id] = []
        memory_id = len(self.storage[user_id])
        self.storage[user_id].append({"memory": memory, "metadata": metadata or {}})
        return memory_id

    def retrieve(self, memory_id: int, user_id: str = "default") -> Optional[Any]:
        user_memories = self.storage.get(user_id, [])
        if 0 <= memory_id < len(user_memories):
            return user_memories[memory_id]
        return None

    def get_all(self, user_id: str = "default") -> List[Dict[str, Any]]:
        return self.storage.get(user_id, [])

    def add(
        self,
        memory: str,
        user_id: str = "default",
        metadata: Optional[Dict[str, Any]] = None,
    ):
        self.store(memory, user_id, metadata)

    def get_all(self, user_id: str = "default") -> List[Dict[str, Any]]:
        return self.retrieve(user_id)

    def search(self, query: str, user_id: str = "default") -> List[Dict[str, Any]]:
        if not query:
            raise ValueError("Query cannot be null or empty.")
        return [
            mem
            for mem in self.storage.get(user_id, [])
            if query.lower() in mem["memory"].lower()
        ]

    def update(self, memory_id: int, data: str, user_id: str = "default"):
        if user_id in self.storage and 0 <= memory_id < len(self.storage[user_id]):
            self.storage[user_id][memory_id]["memory"] = data

    def history(self, memory_id: int, user_id: str = "default") -> List[str]:
        if user_id in self.storage and 0 <= memory_id < len(self.storage[user_id]):
            return [self.storage[user_id][memory_id]["memory"]]
        return []
