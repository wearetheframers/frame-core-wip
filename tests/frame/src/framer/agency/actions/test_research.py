import pytest
from unittest.mock import AsyncMock, Mock, patch
from frame.src.framer.brain.actions.research import ResearchAction
from frame.src.services import ExecutionContext


@pytest.fixture
def mock_execution_context():
    context = Mock(spec=ExecutionContext)
    context.llm_service = AsyncMock()
    context.llm_service.get_completion.return_value = "Mock research results"
    context.llm_service.default_model = "gpt-3.5-turbo"
    context.memory_service = AsyncMock()
    return context


@pytest.mark.asyncio
@patch("builtins.print")
async def test_research(mock_print, mock_execution_context):
    topic = "AI and Machine Learning"
    research_action = ResearchAction()
    result = await research_action.execute(mock_execution_context, topic=topic)

    mock_print.assert_called_once_with(f"Performing research on topic: {topic}")
    mock_execution_context.llm_service.get_completion.assert_called_once_with(
        f"Provide a summary of the latest developments and top libraries for {topic}",
        model="gpt-3.5-turbo",
    )
    mock_execution_context.memory_service.add_memory.assert_called_once_with(
        f"Research on {topic}", "Mock research results"
    )
    assert result == f"Research findings for topic '{topic}':\nMock research results"
