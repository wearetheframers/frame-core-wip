import pytest
from unittest.mock import AsyncMock, Mock
from frame.src.framer.brain.actions.adaptive_decision import (
    AdaptiveDecisionAction,
)
from frame.src.services.context.execution_context_service import ExecutionContext


@pytest.fixture
def mock_execution_context():
    return Mock(spec=ExecutionContext)


@pytest.mark.asyncio
async def test_aggressive_strategy(mock_execution_context):
    action = AdaptiveDecisionAction()
    mock_execution_context.get_full_state.return_value = {
        "urgency": 8,
        "risk": 6,
        "resources": "scarce",
    }
    decision = await action.execute(mock_execution_context)
    assert decision["strategy"] == "aggressive"


@pytest.mark.asyncio
async def test_conservative_strategy(mock_execution_context):
    action = AdaptiveDecisionAction()
    mock_execution_context.get_full_state.return_value = {
        "urgency": 2,
        "risk": 1,
        "resources": "abundant",
    }
    decision = await action.execute(mock_execution_context)
    assert decision["strategy"] == "conservative"


@pytest.mark.asyncio
async def test_balanced_strategy(mock_execution_context):
    action = AdaptiveDecisionAction()
    mock_execution_context.get_full_state.return_value = {
        "urgency": 5,
        "risk": 5,
        "resources": "moderate",
    }
    decision = await action.execute(mock_execution_context)
    assert decision["strategy"] == "balanced"
