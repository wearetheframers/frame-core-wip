import pytest
from frame.src.framer.brain.memory.memory import Memory
from frame.src.framer.brain.memory.memory_adapters.mem0.mem0 import Mem0Adapter
from unittest.mock import Mock, patch
from frame.src.services import ExecutionContext


@pytest.fixture
def memory():
    config = {"adapter": "mem0"}
    return Memory(config)


def test_memory_initialization(memory):
    assert isinstance(memory, Memory)
    assert memory.core == {}
    assert memory.short_term == []
    assert isinstance(memory.mem0, Mem0Adapter)


def test_get_core_memory(memory):
    memory.core = {"test_key": "test_value"}
    assert memory.get_core_memory("test_key") == "test_value"
    assert memory.get_core_memory("non_existent_key") is None


def test_add_long_term_memory(memory):
    with patch.object(memory.mem0, "add") as mock_add:
        memory.add_long_term_memory(
            "test memory", user_id="test_user", metadata={"key": "value"}
        )
        mock_add.assert_called_once_with(
            "test memory", user_id="test_user", metadata={"key": "value"}
        )


def test_add_short_term_memory(memory):
    memory.add_short_term_memory({"key": "value"})
    assert memory.short_term == [{"key": "value"}]

    # Test limit of 10 items
    for i in range(15):
        memory.add_short_term_memory({"key": f"value{i}"})
    assert len(memory.short_term) == 10
    assert memory.short_term[0] == {"key": "value5"}


def test_get_all_memories(memory):
    memory.core = {"core_key": "core_value"}
    memory.short_term = [{"short_term_key": "short_term_value"}]
    with patch.object(
        memory.mem0, "get_all", return_value=[{"long_term_key": "long_term_value"}]
    ):
        all_memories = memory.get_all_memories()
        assert all_memories == {
            "core": {"core_key": "core_value"},
            "long_term": [{"long_term_key": "long_term_value"}],
            "short_term": [{"short_term_key": "short_term_value"}],
        }


def test_search_memories(memory):
    with patch.object(memory.mem0, "search", return_value=[{"result": "test"}]):
        result = memory.search_memories("query", user_id="test_user")
        assert result == [{"result": "test"}]
        memory.mem0.search.assert_called_once_with("query", user_id="test_user")


def test_update_memory(memory):
    with patch.object(memory.mem0, "update") as mock_update:
        memory.update_memory("memory_id", "updated_data")
        mock_update.assert_called_once_with(memory_id="memory_id", data="updated_data")


def test_get_memory_history(memory):
    with patch.object(memory.mem0, "history", return_value=[{"history": "test"}]):
        result = memory.get_memory_history("memory_id")
        assert result == [{"history": "test"}]
        memory.mem0.history.assert_called_once_with(memory_id="memory_id")
