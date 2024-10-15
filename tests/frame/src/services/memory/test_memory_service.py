import pytest
from unittest.mock import Mock
from frame.src.services.memory.main import MemoryService


@pytest.fixture
def mock_adapter():
    adapter = Mock()
    adapter.add = Mock()
    adapter.get_all = Mock()
    adapter.search = Mock()
    adapter.update = Mock()
    adapter.history = Mock()
    return adapter


@pytest.fixture
def memory_service(mock_adapter):
    return MemoryService(mock_adapter)


def test_add_memory(memory_service, mock_adapter):
    memory_service.add_memory("Test memory", "user1", {"tag": "test"})
    mock_adapter.add.assert_called_once_with("Test memory", "user1", {"tag": "test"})


def test_get_all_memories(memory_service, mock_adapter):
    mock_adapter.get_all.return_value = [{"id": 1, "memory": "Test memory"}]
    result = memory_service.get_all_memories("user1")
    assert result == [{"id": 1, "memory": "Test memory"}]
    mock_adapter.get_all.assert_called_once_with("user1")


def test_search_memories(memory_service, mock_adapter):
    mock_adapter.search.return_value = [{"id": 1, "memory": "Test memory"}]
    result = memory_service.search_memories("test", "user1")
    assert result == [{"id": 1, "memory": "Test memory"}]
    mock_adapter.search.assert_called_once_with("test", "user1")


def test_update_memory(memory_service, mock_adapter):
    memory_service.update_memory(1, "Updated memory", "user1")
    mock_adapter.update.assert_called_once_with(1, "Updated memory", "user1")


def test_get_memory_history(memory_service, mock_adapter):
    mock_adapter.history.return_value = ["Original memory", "Updated memory"]
    result = memory_service.get_memory_history(1, "user1")
    assert result == ["Original memory", "Updated memory"]
    mock_adapter.history.assert_called_once_with(1, "user1")
