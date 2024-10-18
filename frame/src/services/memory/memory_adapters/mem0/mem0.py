from typing import Dict, Any, List, Optional


from typing import Any, Dict, List, Optional

class Mem0Adapter:
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
    ):
        if user_id not in self.storage:
            self.storage[user_id] = []
        self.storage[user_id].append({"memory": memory, "metadata": metadata or {}})

    def retrieve(self, user_id: str = "default") -> List[Dict[str, Any]]:
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
