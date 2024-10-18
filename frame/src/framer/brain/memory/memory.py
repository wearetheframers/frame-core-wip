import logging
from typing import Dict, Any, List, Optional
from typing import Dict, Any, List, Optional
from frame.src.framer.brain.memory.memory_adapters.mem0.mem0_adapter import Mem0Adapter

logger = logging.getLogger(__name__)


class Memory:
    """
    The Memory class manages memory storage and retrieval for Framers.

    It supports both global and multi-user memory contexts. When no user ID is provided,
    memories are stored in a global context. When multiple user IDs are provided, the
    memory retrieval process searches across all specified user IDs.

    This is achieved using the Mem0Adapter, which abstracts away the
    underlying storage solution and provides a flexible interface for memory operations.
    """

    def __init__(self, config: Dict[str, Any]):
        self.core = {}
        self.short_term = []
        self.mem0 = Mem0Adapter()
        self.user_id = config.get("user_id", "default")

    def get_core_memory(self, key: str) -> Any:
        """
        Retrieve a specific core memory by its key.

        Args:
            key (str): The key of the memory to retrieve.

        Returns:
            Any: The retrieved memory data, or None if not found.
        """
        core_memory = self.core.get(key)
        if core_memory is not None:
            return core_memory

        mem0_data = self.mem0.get_all(user_id=self.user_id)
        for memory_id, item in enumerate(mem0_data):
            if isinstance(item, dict) and item.get("metadata", {}).get("key") == key:
                return item.get("memory")
        return None

    def set_core_memory(self, key: str, value: Any) -> Any:
        """
        Set a value in core memory.

        Args:
            key (str): The key to store the memory under.
            value (Any): The value to store in memory.

        Returns:
            Any: The stored value.
        """
        self.core[key] = value
        self.mem0.store(str(value), user_id=self.user_id, metadata={"key": key})
        return value

    def retrieve_memory(self, key: str) -> Any:
        """
        Alias for get_core_memory for backward compatibility.

        Args:
            key (str): The key of the memory to retrieve.

        Returns:
            Any: The retrieved memory data, or None if not found.
        """
        return self.get_core_memory(key)

    def add_long_term_memory(
        self,
        memory: str,
        user_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        self.mem0.store(memory, user_id=user_id or self.user_id, metadata=metadata)

    def add_short_term_memory(self, memory: Dict[str, Any]):
        self.short_term.append(memory)
        if len(self.short_term) > 10:  # Limit short-term memory to last 10 items
            self.short_term.pop(0)

    def get_all_memories(self) -> Dict[str, Any]:
        return {
            "core": self.core,
            "long_term": self.mem0.get_all(user_id=self.user_id),
            "short_term": self.short_term,
        }

    def search_memories(
        self, query: str, user_id: str = "default"
    ) -> List[Dict[str, Any]]:
        core_results = [
            {"memory": v, "source": "core"}
            for k, v in self.core.items()
            if query.lower() in str(v).lower()
        ]
        mem0_results = self.mem0.search(query, user_id=user_id)
        return core_results + mem0_results

    def update_memory(self, key: str, value: str):
        self.core[key] = value
        self.mem0.update(memory_id=key, data=value)

    def get_memory_history(self, memory_id: int) -> List[str]:
        return self.mem0.history(memory_id=memory_id)
