import pytest
from unittest.mock import Mock
from frame.src.framer.brain.actions.create_new_agent import CreateNewAgentAction
from frame.src.framer.config import FramerConfig
from frame.src.services import ExecutionContext


@pytest.fixture
def mock_framer():
    framer = Mock()
    framer.create_framer = Mock()
    return framer


def test_create_new_agent(mock_framer):
    config = {"name": "Test Framer", "model": "gpt-3.5-turbo"}
    create_new_agent_action = CreateNewAgentAction()
    result = create_new_agent_action.execute(mock_framer, config)

    mock_framer.create_framer.assert_called_once_with(FramerConfig(**config))
    assert result == mock_framer.create_framer.return_value
