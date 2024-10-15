from typing import Dict, Any, List, Optional
from frame.src.framer.brain.memory.memory_adapter_interface import (
    MemoryAdapterInterface,
)


class Mem0Adapter(MemoryAdapterInterface):
    """
    Mem0Adapter is responsible for interfacing with the Mem0 memory system.
    It provides methods to store, retrieve, and manage memory data.
    """

    def __init__(self):
        self.memories = {}

    def store(
        self,
        memory: str,
        user_id: str = "default",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> int:
        """
        Store a new memory entry in the Mem0 system.

        Args:
            memory (str): The memory content to store.
            user_id (str, optional): The user ID associated with the memory. Defaults to "default".
            metadata (Optional[Dict[str, Any]], optional): Metadata for the memory. Defaults to None.

        Returns:
            int: The ID of the stored memory.
        """
        return self.add(memory, user_id, metadata)

    def add(
        self,
        memory: str,
        user_id: str = "default",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> int:
        """
        Add a new memory entry in the Mem0 system.

        Args:
            memory (str): The memory content to add.
            user_id (str, optional): The user ID associated with the memory. Defaults to "default".
            metadata (Optional[Dict[str, Any]], optional): Metadata for the memory. Defaults to None.

        Returns:
            int: The ID of the added memory.
        """
        if user_id not in self.memories:
            self.memories[user_id] = []
        memory_id = len(self.memories[user_id])
        self.memories[user_id].append({"memory": memory, "metadata": metadata or {}})
        return memory_id

    def retrieve(self, memory_id: int, user_id: str = "default") -> Optional[Any]:
        """
        Retrieve a specific memory entry from the Mem0 system.

        Args:
            memory_id (int): The ID of the memory to retrieve.
            user_id (str, optional): The user ID associated with the memory. Defaults to "default".

        Returns:
            Optional[Any]: The retrieved memory content, or None if not found.
        """
        if user_id in self.memories and 0 <= memory_id < len(self.memories[user_id]):
            return self.memories[user_id][memory_id]["memory"]
        return None

    def update(self, memory_id: int, data: Any, user_id: str = "default") -> None:
        """
        Update a specific memory entry.

        Args:
            memory_id (int): The ID of the memory to update.
            data (Any): The new memory content.
            user_id (str, optional): The user ID associated with the memory. Defaults to "default".
        """
        if user_id in self.memories and 0 <= memory_id < len(self.memories[user_id]):
            self.memories[user_id][memory_id]["memory"] = data

    def delete(self, memory_id: int, user_id: str = "default") -> None:
        """
        Delete a specific memory entry.

        Args:
            memory_id (int): The ID of the memory to delete.
            user_id (str, optional): The user ID associated with the memory. Defaults to "default".
        """
        if user_id in self.memories and 0 <= memory_id < len(self.memories[user_id]):
            del self.memories[user_id][memory_id]

    def get_all(self, user_id: str = "default") -> List[Dict[str, Any]]:
        """
        Retrieve all memory entries for a specific user from the Mem0 system.

        Args:
            user_id (str, optional): The user ID to retrieve memories for. Defaults to "default".

        Returns:
            List[Dict[str, Any]]: A list of all memory entries for the specified user.
        """
        return self.memories.get(user_id, [])

    def search(self, query: str, user_id: str = "default") -> List[Dict[str, Any]]:
        """
        Search for memory entries containing the query string for a specific user.

        Args:
            query (str): The search query string.
            user_id (str, optional): The user ID to search memories for. Defaults to "default".

        Returns:
            List[Dict[str, Any]]: A list of memory entries that match the search query.
        """
        return [
            mem
            for mem in self.memories.get(user_id, [])
            if query.lower() in str(mem["memory"]).lower()
        ]

    def history(self, memory_id: int, user_id: str = "default") -> List[str]:
        """
        Retrieve the history of a specific memory entry.

        Args:
            memory_id (int): The ID of the memory to retrieve history for.
            user_id (str, optional): The user ID associated with the memory. Defaults to "default".

        Returns:
            List[str]: A list containing the memory content (as we don't store history in this simple implementation).
        """
        if user_id in self.memories and 0 <= memory_id < len(self.memories[user_id]):
            return [str(self.memories[user_id][memory_id]["memory"])]
        return []
