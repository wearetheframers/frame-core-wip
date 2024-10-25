import pytest
from unittest.mock import AsyncMock, MagicMock
from frame.src.framer.brain.actions.observe import ObserveAction
from frame.src.services import ExecutionContext


@pytest.fixture
def execution_context():
    context = MagicMock(spec=ExecutionContext)
    context.llm_service = AsyncMock()
    return context


@pytest.fixture
def observe_action():
    return ObserveAction()


@pytest.mark.asyncio
async def test_observe_action_with_observation():
    """Test observe action with a valid observation"""
    # Arrange
    action = ObserveAction()
    context = MagicMock(spec=ExecutionContext)
    observation = "Test observation"
    insights = {"key": "value"}

    # Act
    result = await action.execute(context, observation=observation, insights=insights)

    # Assert
    assert isinstance(result, str)
    assert "Test observation" in result
    assert "key: value" in str(result)


@pytest.mark.asyncio
async def test_observe_action_without_inputs():
    """Test observe action with no inputs"""
    # Arrange
    action = ObserveAction()
    context = MagicMock(spec=ExecutionContext)

    # Act
    result = await action.execute(context)

    # Assert
    assert "Observation skipped" in result


@pytest.mark.asyncio
async def test_observe_action_with_only_insights():
    """Test observe action with only insights provided"""
    # Arrange
    action = ObserveAction()
    context = MagicMock(spec=ExecutionContext)
    insights = {"test": "insight"}

    # Act
    result = await action.execute(context, insights=insights)

    # Assert
    assert isinstance(result, str)
    assert "Additional insights" in result


@pytest.mark.asyncio
async def test_observe_action_priority():
    """Test that observe action has correct priority"""
    # Arrange
    action = ObserveAction()

    # Assert
    assert action.priority == 1
