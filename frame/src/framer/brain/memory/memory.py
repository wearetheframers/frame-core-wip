import logging
from typing import Dict, Any, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from frame.src.services import MemoryService

# Import MemoryService inside the __init__ method to avoid circular import issues
from .memory_adapter_interface import MemoryAdapterInterface

__all__ = ["MemoryAdapterInterface", "Memory"]

logger = logging.getLogger(__name__)


class Memory:
    """
    The Memory class manages memory storage and retrieval for Framers.

    It supports both global and multi-user memory contexts. When no user ID is provided,
    memories are stored in a global context. When multiple user IDs are provided, the
    memory retrieval process searches across all specified user IDs.

    This class now uses the MemoryService for all memory operations.
    """

    def __init__(self, memory_service: Optional["MemoryService"] = None):
        self.core = None  # Initialize core attribute
        self.mem0 = None  # Initialize mem0 attribute
        if memory_service is None:
            from frame.src.services.memory.main import MemoryService

            memory_service = MemoryService()
        self.memory_service = memory_service
        self.user_id = "default"

    def store(
        self,
        memory: str,
        user_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """
        Store a memory using the memory service.

        Args:
            memory (str): The memory to store.
            user_id (Optional[str]): The user ID to associate with the memory.
            metadata (Optional[Dict[str, Any]]): Additional metadata for the memory.
        """
        if self.memory_service:
            self.memory_service.add_memory(memory, user_id or self.user_id, metadata)
        else:
            logger.warning("Memory service is not initialized. Unable to store memory.")

    def retrieve(
        self, query: str, user_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve memories based on a query.

        Args:
            query (str): The query to search for in memories.
            user_id (Optional[str]): The user ID to search memories for.

        Returns:
            List[Dict[str, Any]]: A list of matching memories.
        """
        return self.memory_service.search(query, user_id or self.user_id)

    def update(self, memory_id: str, memory: str, user_id: Optional[str] = None):
        """
        Update an existing memory.

        Args:
            memory_id (str): The ID of the memory to update.
            memory (str): The updated memory content.
            user_id (Optional[str]): The user ID associated with the memory.
        """
        self.memory_service.update(memory_id, memory, user_id or self.user_id)

    def delete(self, memory_id: str, user_id: Optional[str] = None):
        """
        Delete a memory.

        Args:
            memory_id (str): The ID of the memory to delete.
            user_id (Optional[str]): The user ID associated with the memory.
        """
        self.memory_service.delete(memory_id, user_id or self.user_id)

    def get_core_memory(self) -> Any:
        """
        Get the core memory.

        Returns:
            Any: The core memory object.
        """
        return self.core

    def add_short_term_memory(self, memory: str, user_id: Optional[str] = None):
        """
        Add a short-term memory.

        Args:
            memory (str): The memory to add.
            user_id (Optional[str]): The user ID to associate with the memory.
        """
        # Implementation for adding short-term memory
        pass

    def get_all_memories(self, user_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get all memories for a user.

        Args:
            user_id (Optional[str]): The user ID to get memories for.

        Returns:
            List[Dict[str, Any]]: A list of all memories for the user.
        """
        return self.memory_service.get_all(user_id or self.user_id)
