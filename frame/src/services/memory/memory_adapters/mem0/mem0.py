from typing import Dict, Any, List, Optional


from typing import Any, Dict, List, Optional

class Mem0Adapter:
    """
    Adapter for basic memory operations.

    This class provides methods to interact with the memory storage,
    including adding, retrieving, and searching memories.
    """

    def __init__(self):
        self.memories = {}

    def store(self, memory: str, user_id: str = "default", metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Store a memory in the adapter.

        Args:
            memory (str): The memory to store.
            user_id (str): The ID of the user associated with the memory.
            metadata (Optional[Dict[str, Any]]): Additional metadata for the memory.
        """
        if user_id not in self.memories:
            self.memories[user_id] = []
        self.memories[user_id].append({"content": memory, "metadata": metadata or {}})

    def retrieve(self, user_id: str = "default", query: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Retrieve memories from the adapter.

        Args:
            user_id (str): The ID of the user whose memories to retrieve.
            query (Optional[str]): A query string to filter memories (not implemented in this basic version).

        Returns:
            List[Dict[str, Any]]: A list of memories with their metadata.
        """
        return self.memories.get(user_id, [])
    """

    def __init__(self):
        self.storage = {}

    def add(
        self,
        memory: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Add a memory to the storage.

        Args:
            memory (str): The memory to store.
            metadata (Optional[Dict[str, Any]]): Additional metadata for the memory.
        """
        self.mem0.store(memory, self.user_id, metadata)

    def get_memories(self) -> List[Dict[str, Any]]:
        """
        Retrieve all memories for the current user.

        Returns:
            List[Dict[str, Any]]: A list of memories with their metadata.
        """
        return self.mem0.retrieve(self.user_id)
    ):
        if user_id not in self.storage:
            self.storage[user_id] = []
        self.storage[user_id].append({"memory": memory, "metadata": metadata or {}})

    """
    Adapter for basic memory operations.

    This class provides methods to interact with the memory storage,
    including adding, retrieving, and searching memories.
    """

    def __init__(self):
        self.storage = {}

    def add(
        self,
        memory: str,
        user_id: str = "default",
        metadata: Optional[Dict[str, Any]] = None,
    ):
        if user_id not in self.storage:
            self.storage[user_id] = []
        self.storage[user_id].append({"memory": memory, "metadata": metadata or {}})

    def get_all(self, user_id: str = "default") -> List[Dict[str, Any]]:
        return self.storage.get(user_id, [])

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
