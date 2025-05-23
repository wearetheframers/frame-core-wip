import pytest
from unittest.mock import AsyncMock, MagicMock
from frame.src.framer.brain.actions.respond import RespondAction
from frame.src.services import ExecutionContext


@pytest.fixture
def mock_execution_context():
    context = MagicMock(spec=ExecutionContext)
    context.llm_service = AsyncMock()
    context.get_state = MagicMock(return_value="No recent perception available.")
    context.memory_service = MagicMock()
    context.memory_service.get_recent_memories = MagicMock(return_value=[])
    context.soul = MagicMock()
    context.soul.get_current_state = MagicMock(return_value={})
    return context


@pytest.mark.asyncio
async def test_respond(mock_execution_context):
    mock_execution_context.llm_service.get_completion.return_value = (
        "Generated response"
    )

    respond_action = RespondAction()
    result = await respond_action.execute(mock_execution_context)

    assert isinstance(result, dict)
    assert "response" in result
    assert result["response"] == "Generated response"

    # Verify that the LLM service was called with the correct prompt
    mock_execution_context.llm_service.get_completion.assert_called_once()
    prompt = mock_execution_context.llm_service.get_completion.call_args[0][0]
    assert "As an AI assistant with the following characteristics:" in prompt
    assert (
        "Please generate a response that takes into account all of the above information"
        in prompt
    )
