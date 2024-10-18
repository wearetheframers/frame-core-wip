from typing import Any, Dict, List, Optional
from frame.src.framer.brain.memory.memory_adapter_interface import (
    MemoryAdapterInterface,
)
from mem0 import Memory
from frame.src.constants.api_keys import MEM0_SERVER_HOST


class Mem0Adapter(MemoryAdapterInterface):
    """
    Mem0Adapter is responsible for interfacing with the Mem0 memory system.
    It provides methods to store, retrieve, and manage memory data.
    """

    def __init__(self, api_key: str):
        if MEM0_SERVER_HOST:
            self.client = Memory(api_key=api_key, server_url=MEM0_SERVER_HOST)
        else:
            self.client = Memory(api_key=api_key)

    def add(
        self,
        memory: str,
        user_id: str = "default",
        metadata: Optional[Dict[str, Any]] = None,
        run_id: Optional[str] = None,
        agent_id: Optional[str] = None,
        output_format: str = "v1.1",
    ) -> Dict[str, Any]:
        """
        Add a new memory to the Mem0 system.

        Args:
            memory (str): The memory content to be added.
            user_id (str): The ID of the user associated with this memory.
            metadata (Optional[Dict[str, Any]]): Additional metadata for the memory.
            run_id (Optional[str]): The ID of the run (session) associated with this memory.
            agent_id (Optional[str]): The ID of the agent associated with this memory.
            output_format (str): The output format version to use.

        Returns:
            Dict[str, Any]: The response from the Mem0 system.
        """
        messages = [{"role": "user", "content": memory}]
        kwargs = {"output_format": output_format}
        if user_id:
            kwargs["user_id"] = user_id
        if run_id:
            kwargs["run_id"] = run_id
        if agent_id:
            kwargs["agent_id"] = agent_id
        return self.client.add(messages, **kwargs)

    def search(
        self,
        query: str,
        user_id: Optional[str] = None,
        agent_id: Optional[str] = None,
        run_id: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 5,
        output_format: str = "v1.1",
    ) -> List[Dict[str, Any]]:
        """
        Search for memories in the Mem0 system.

        Args:
            query (str): The search query.
            user_id (Optional[str]): The ID of the user to search memories for.
            agent_id (Optional[str]): The ID of the agent to search memories for.
            run_id (Optional[str]): The ID of the run (session) to search memories for.
            filters (Optional[Dict[str, Any]]): Additional filters for the search.
            limit (int): The maximum number of results to return.
            output_format (str): The output format version to use.

        Returns:
            List[Dict[str, Any]]: A list of matching memories.
        """
        kwargs = {"output_format": output_format}
        if user_id:
            kwargs["user_id"] = user_id
        if agent_id:
            kwargs["agent_id"] = agent_id
        if run_id:
            kwargs["run_id"] = run_id
        if filters:
            kwargs["version"] = "v2"
            kwargs["filters"] = filters
        results = self.client.search(query, **kwargs)
        return results[:limit]

    def get_all(
        self,
        user_id: Optional[str] = None,
        agent_id: Optional[str] = None,
        run_id: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None,
        output_format: str = "v1.1",
    ) -> List[Dict[str, Any]]:
        """
        Retrieve all memories for a specific user, agent, or run.

        Args:
            user_id (Optional[str]): The ID of the user to retrieve memories for.
            agent_id (Optional[str]): The ID of the agent to retrieve memories for.
            run_id (Optional[str]): The ID of the run (session) to retrieve memories for.
            filters (Optional[Dict[str, Any]]): Additional filters for retrieval.
            output_format (str): The output format version to use.

        Returns:
            List[Dict[str, Any]]: A list of all memories for the specified parameters.
        """
        kwargs = {"output_format": output_format}
        if user_id:
            kwargs["user_id"] = user_id
        if agent_id:
            kwargs["agent_id"] = agent_id
        if run_id:
            kwargs["run_id"] = run_id
        if filters:
            kwargs["version"] = "v2"
            kwargs["filters"] = filters
        return self.client.get_all(**kwargs)

    def delete(self, memory_id: str) -> Dict[str, Any]:
        """
        Delete a specific memory.

        Args:
            memory_id (str): The ID of the memory to delete.

        Returns:
            Dict[str, Any]: The response from the Mem0 system.
        """
        return self.client.delete(memory_id)

    def delete_all(
        self,
        user_id: Optional[str] = None,
        agent_id: Optional[str] = None,
        run_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Delete all memories for a specific user, agent, or run.

        Args:
            user_id (Optional[str]): The ID of the user to delete memories for.
            agent_id (Optional[str]): The ID of the agent to delete memories for.
            run_id (Optional[str]): The ID of the run (session) to delete memories for.

        Returns:
            Dict[str, Any]: The response from the Mem0 system.
        """
        kwargs = {}
        if user_id:
            kwargs["user_id"] = user_id
        if agent_id:
            kwargs["agent_id"] = agent_id
        if run_id:
            kwargs["run_id"] = run_id
        return self.client.delete_all(**kwargs)

    def get_users(self) -> List[Dict[str, Any]]:
        """
        Get all users, agents, and runs which have memories associated with them.

        Returns:
            List[Dict[str, Any]]: A list of users, agents, and runs.
        """
        return self.client.users()

    def get_memory(self, memory_id: str) -> Dict[str, Any]:
        """
        Get a specific memory by its ID.

        Args:
            memory_id (str): The ID of the memory to retrieve.

        Returns:
            Dict[str, Any]: The memory data.
        """
        return self.client.get(memory_id)

    def update(self, memory_id: str, new_content: str) -> Dict[str, Any]:
        """
        Update a specific memory with new content.

        Args:
            memory_id (str): The ID of the memory to update.
            new_content (str): The new content for the memory.

        Returns:
            Dict[str, Any]: The response from the Mem0 system.
        """
        return self.client.update(memory_id, new_content)

    def get_history(self, memory_id: str) -> List[Dict[str, Any]]:
        """
        Get the history of how a memory has changed over time.

        Args:
            memory_id (str): The ID of the memory to get history for.

        Returns:
            List[Dict[str, Any]]: A list of historical versions of the memory.
        """
        return self.client.history(memory_id)

    def reset(self) -> Dict[str, Any]:
        """
        Reset the Mem0 client.

        Returns:
            Dict[str, Any]: The response from the Mem0 system.
        """
        return self.client.reset()
