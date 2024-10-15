import pytest
from frame.src.services.memory.memory_adapters.mem0.mem0 import Mem0Adapter


@pytest.fixture
def mem0_adapter():
    return Mem0Adapter()


def test_add_and_get_all(mem0_adapter):
    mem0_adapter.add("Test memory 1")
    mem0_adapter.add("Test memory 2", user_id="user1")

    assert len(mem0_adapter.get_all()) == 1
    assert len(mem0_adapter.get_all("user1")) == 1
    assert mem0_adapter.get_all()[0]["memory"] == "Test memory 1"
    assert mem0_adapter.get_all("user1")[0]["memory"] == "Test memory 2"


def test_search(mem0_adapter):
    mem0_adapter.add("Apple pie recipe")
    mem0_adapter.add("Banana smoothie recipe")

    results = mem0_adapter.search("Apple")
    assert len(results) == 1
    assert results[0]["memory"] == "Apple pie recipe"


def test_update(mem0_adapter):
    mem0_adapter.add("Original memory")
    mem0_adapter.update(0, "Updated memory")

    assert mem0_adapter.get_all()[0]["memory"] == "Updated memory"


def test_history(mem0_adapter):
    mem0_adapter.add("Test memory")

    history = mem0_adapter.history(0)
    assert len(history) == 1
    assert history[0] == "Test memory"


def test_add_with_metadata(mem0_adapter):
    metadata = {"importance": "high", "category": "recipe"}
    mem0_adapter.add("Chocolate cake recipe", metadata=metadata)

    memory = mem0_adapter.get_all()[0]
    assert memory["memory"] == "Chocolate cake recipe"
    assert memory["metadata"] == metadata


def test_search_with_user_id(mem0_adapter):
    mem0_adapter.add("User1 memory", user_id="user1")
    mem0_adapter.add("User2 memory", user_id="user2")

    results = mem0_adapter.search("memory", user_id="user1")
    assert len(results) == 1
    assert results[0]["memory"] == "User1 memory"


def test_update_with_user_id(mem0_adapter):
    mem0_adapter.add("Original user1 memory", user_id="user1")
    mem0_adapter.update(0, "Updated user1 memory", user_id="user1")

    assert mem0_adapter.get_all("user1")[0]["memory"] == "Updated user1 memory"


def test_history_with_user_id(mem0_adapter):
    mem0_adapter.add("User1 memory", user_id="user1")

    history = mem0_adapter.history(0, user_id="user1")
    assert len(history) == 1
    assert history[0] == "User1 memory"


def test_add_multiple_memories(mem0_adapter):
    mem0_adapter.add("Memory 1")
    mem0_adapter.add("Memory 2")
    mem0_adapter.add("Memory 3")

    all_memories = mem0_adapter.get_all()
    assert len(all_memories) == 3
    assert [m["memory"] for m in all_memories] == ["Memory 1", "Memory 2", "Memory 3"]


def test_search_case_insensitive(mem0_adapter):
    mem0_adapter.add("Apple pie recipe")
    mem0_adapter.add("APPLE juice recipe")

    results = mem0_adapter.search("apple")
    assert len(results) == 2
    assert set(m["memory"] for m in results) == {
        "Apple pie recipe",
        "APPLE juice recipe",
    }
