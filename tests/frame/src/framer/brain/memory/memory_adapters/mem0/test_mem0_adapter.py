import pytest
from frame.src.framer.brain.memory.memory_adapters.mem0_adapter.mem0_adapter import (
    Mem0Adapter,
)
from frame.src.services import ExecutionContext


@pytest.fixture
def mem0_adapter():
    return Mem0Adapter()


def test_add_and_get_all(mem0_adapter):
    mem0_adapter.add("Memory 1", "user1")
    mem0_adapter.add("Memory 2", "user1")
    mem0_adapter.add("Memory 3", "user2")

    user1_memories = mem0_adapter.get_all("user1")
    user2_memories = mem0_adapter.get_all("user2")

    assert len(user1_memories) == 2
    assert len(user2_memories) == 1
    assert user1_memories[0]["memory"] == "Memory 1"
    assert user1_memories[1]["memory"] == "Memory 2"
    assert user2_memories[0]["memory"] == "Memory 3"


def test_add_with_metadata(mem0_adapter):
    metadata = {"tag": "important"}
    mem0_adapter.add("Memory with metadata", "user1", metadata)

    user1_memories = mem0_adapter.get_all("user1")
    assert len(user1_memories) == 1
    assert user1_memories[0]["memory"] == "Memory with metadata"
    assert user1_memories[0]["metadata"] == metadata


def test_search(mem0_adapter):
    mem0_adapter.add("Apple pie recipe", "user1")
    mem0_adapter.add("Banana smoothie recipe", "user1")
    mem0_adapter.add("Apple juice recipe", "user1")

    search_results = mem0_adapter.search("Apple", "user1")
    assert len(search_results) == 2
    assert "Apple pie recipe" in [mem["memory"] for mem in search_results]
    assert "Apple juice recipe" in [mem["memory"] for mem in search_results]


def test_update(mem0_adapter):
    mem0_adapter.add("Original memory", "user1")
    mem0_adapter.update(0, "Updated memory", "user1")

    user1_memories = mem0_adapter.get_all("user1")
    assert len(user1_memories) == 1
    assert user1_memories[0]["memory"] == "Updated memory"


def test_history(mem0_adapter):
    mem0_adapter.add("Memory 1", "user1")
    history = mem0_adapter.history(0, "user1")
    assert len(history) == 1
    assert history[0] == "Memory 1"


def test_nonexistent_user(mem0_adapter):
    assert mem0_adapter.get_all("nonexistent_user") == []
    assert mem0_adapter.search("query", "nonexistent_user") == []
    assert mem0_adapter.history(0, "nonexistent_user") == []


def test_update_nonexistent_memory(mem0_adapter):
    mem0_adapter.add("Memory 1", "user1")
    mem0_adapter.update(1, "Updated memory", "user1")  # This should not raise an error
    user1_memories = mem0_adapter.get_all("user1")
    assert len(user1_memories) == 1
    assert (
        user1_memories[0]["memory"] == "Memory 1"
    )  # The original memory should remain unchanged


def test_update_nonexistent_user(mem0_adapter):
    mem0_adapter.update(
        0, "Updated memory", "nonexistent_user"
    )  # This should not raise an error
    assert mem0_adapter.get_all("nonexistent_user") == []


def test_history_nonexistent_user(mem0_adapter):
    history = mem0_adapter.history(0, "nonexistent_user")
    assert history == []
