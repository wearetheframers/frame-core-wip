import pytest
from frame.src.framer.soul.soul import Soul
from frame.src.framer.agency.execution_context import ExecutionContext


@pytest.fixture
def sample_soul():
    return Soul(seed={"seed": "Test seed"})


def test_soul_initialization(sample_soul):
    assert sample_soul.seed["text"] == "Test seed"
    assert isinstance(sample_soul.state, dict)
    assert sample_soul.model.essence == "Test seed"


def test_update_state(sample_soul):
    sample_soul.update_state("test_key", "test_value")
    assert sample_soul.state["test_key"] == "test_value"


def test_get_state(sample_soul):
    sample_soul.update_state("test_key", "test_value")
    assert sample_soul.get_state("test_key") == "test_value"
    assert sample_soul.get_state("non_existent_key") is None


def test_get_current_state(sample_soul):
    sample_soul.update_state("key1", "value1")
    sample_soul.update_state("key2", "value2")
    current_state = sample_soul.get_current_state()
    assert current_state == {"key1": "value1", "key2": "value2"}


def test_generate_state_summary(sample_soul):
    sample_soul.update_state("key1", "value1")
    sample_soul.update_state("key2", "value2")
    summary = sample_soul.generate_state_summary()
    assert "Soul State Summary:" in summary
    assert "Test seed" in summary
    assert "key1" in summary
    assert "value1" in summary
    assert "key2" in summary
    assert "value2" in summary


def test_soul_seed_initialization():
    soul = Soul(seed={"text": "Test soul seed"})
    assert soul.seed == {"text": "Test soul seed"}


def test_empty_initialization():
    soul = Soul()
    assert soul.seed == {"text": "You are a helpful AI assistant."}
    assert isinstance(soul.state, dict)


def test_soul_initialization_with_dict():
    soul = Soul(
        seed={"text": "Test essence", "attribute1": "value1", "attribute2": "value2"}
    )
    assert soul.seed == {"text": "Test essence"}
    assert soul.model.essence == "Test essence"
    assert soul.model.notes == {"attribute1": "value1", "attribute2": "value2"}
