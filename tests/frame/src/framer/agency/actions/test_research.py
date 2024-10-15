import pytest
from unittest.mock import Mock, patch
from frame.src.framer.agency.actions.research import research

@pytest.fixture
def mock_framer():
    return Mock()

@patch('builtins.print')
def test_research(mock_print, mock_framer):
    topic = "AI and Machine Learning"
    result = research(mock_framer, topic)

    mock_print.assert_called_once_with(f"Performing research on topic: {topic}")
    assert result == f"Research findings for topic: {topic}"
