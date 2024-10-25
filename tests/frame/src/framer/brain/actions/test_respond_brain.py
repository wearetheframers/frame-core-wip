import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from frame.src.framer.brain.actions.respond import RespondAction
from frame.src.services import ExecutionContext
from frame.src.framer.soul import Soul

@pytest.fixture
def execution_context():
    context = MagicMock(spec=ExecutionContext)
    context.llm_service = AsyncMock()
    context.soul = MagicMock(spec=Soul)
    context.get_state = MagicMock()
    context.memory_service = MagicMock()
    return context

@pytest.fixture
def respond_action():
    return RespondAction()

@pytest.mark.asyncio
async def test_respond_action_basic_response():
    """Test respond action generates basic response"""
    # Arrange
    action = RespondAction()
    context = MagicMock(spec=ExecutionContext)
    context.llm_service = AsyncMock()
    context.llm_service.get_completion.return_value = "Test response"
    context.soul = MagicMock()
    context.soul.get_current_state.return_value = {}
    context.get_state.return_value = []
    
    # Act
    result = await action.execute(context, content="Test input")
    
    # Assert
    assert isinstance(result, dict)
    assert "response" in result
    assert result["response"] == "Test response"

@pytest.mark.asyncio
async def test_respond_action_with_context():
    """Test respond action uses context properly"""
    # Arrange
    action = RespondAction()
    context = MagicMock(spec=ExecutionContext)
    context.llm_service = AsyncMock()
    context.llm_service.get_completion.return_value = "Contextual response"
    context.soul = MagicMock()
    context.soul.get_current_state.return_value = {"mood": "happy"}
    context.get_state.side_effect = [
        "Recent perception",  # for recent_perception
        [],  # for recent_memories
        [],  # for recent_perceptions
        [],  # for roles
        []   # for goals
    ]
    
    # Act
    result = await action.execute(context)
    
    # Assert
    assert isinstance(result, dict)
    assert "response" in result
    assert result["response"] == "Contextual response"
    assert context.llm_service.get_completion.called

@pytest.mark.asyncio
async def test_respond_action_invalid_context():
    """Test respond action handles invalid execution context"""
    # Arrange
    action = RespondAction()
    invalid_context = "not a context"
    
    # Act/Assert
    with pytest.raises(TypeError):
        await action.execute(invalid_context)

@pytest.mark.asyncio
async def test_respond_action_none_response():
    """Test respond action handles None response from LLM"""
    # Arrange
    action = RespondAction()
    context = MagicMock(spec=ExecutionContext)
    context.llm_service = AsyncMock()
    context.llm_service.get_completion.return_value = None
    context.soul = MagicMock()
    context.soul.get_current_state.return_value = {}
    context.get_state.return_value = []
    
    # Act
    result = await action.execute(context)
    
    # Assert
    assert isinstance(result, dict)
    assert result["response"] == "No response generated."

@pytest.mark.asyncio
async def test_respond_action_priority():
    """Test that respond action has correct priority"""
    # Arrange
    action = RespondAction()
    
    # Assert
    assert action.priority == 2
