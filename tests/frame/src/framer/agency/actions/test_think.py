import pytest
from unittest.mock import Mock
from frame.src.framer.agency.actions.think import think

@pytest.fixture
def mock_framer():
    framer = Mock()
    framer.mind = Mock()
    framer.mind.current_thought = "Generated thought"
    return framer

def test_think(mock_framer):
    thought = "Processing information..."
    result = think(mock_framer, thought)

    mock_framer.mind.think.assert_called_once_with(thought)
    assert result == f"Thought: {mock_framer.mind.current_thought}"

def test_think_default_thought(mock_framer):
    result = think(mock_framer)

    mock_framer.mind.think.assert_called_once_with("Processing information...")
    assert result == f"Thought: {mock_framer.mind.current_thought}"
