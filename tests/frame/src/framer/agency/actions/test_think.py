import pytest
from unittest.mock import Mock, AsyncMock
from frame.src.framer.agency.actions.think import think
from frame.src.framer.agency.action_registry import ActionRegistry
from frame.src.services import ExecutionContext


@pytest.fixture
def mock_framer():
    framer = Mock()
    framer.brain = AsyncMock()
    framer.brain.make_decision = Mock()
    framer.brain._execute_think_action = AsyncMock()
    return framer


@pytest.fixture
def action_registry():
    mock_execution_context = Mock()
    return ActionRegistry(execution_context=mock_execution_context)


@pytest.mark.asyncio
async def test_think(mock_framer):
    thought = "Processing information..."
    mock_framer.brain._execute_think_action.return_value = {"analysis": "Test analysis"}

    result = await think(mock_framer, thought)

    mock_framer.brain.make_decision.assert_called_once_with(
        {"action": "think", "parameters": {"thought": thought}}
    )
    mock_framer.brain._execute_think_action.assert_called_once()
    assert result == {"analysis": "Test analysis"}


@pytest.mark.asyncio
async def test_think_default_thought(mock_framer):
    mock_framer.brain._execute_think_action.return_value = {
        "analysis": "Default analysis"
    }

    result = await think(mock_framer)

    mock_framer.brain.make_decision.assert_called_once_with(
        {"action": "think", "parameters": {"thought": "Processing information..."}}
    )
    mock_framer.brain._execute_think_action.assert_called_once()
    assert result == {"analysis": "Default analysis"}
