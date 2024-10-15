import pytest
from unittest.mock import AsyncMock
from frame.frame import Frame
from frame.src.services.llm.main import LLMService
from frame.src.framer.config import FramerConfig
from frame.src.framer.agency.execution_context import ExecutionContext


@pytest.fixture
def frame():
    return Frame()


def test_frame_initialization(frame):
    assert isinstance(frame, Frame)
    assert isinstance(frame.llm_service, LLMService)
    assert frame.default_model == "gpt-3.5-turbo"
    assert frame.llm_service.default_model == "gpt-3.5-turbo"


def test_frame_initialization_with_custom_model():
    custom_frame = Frame(default_model="gpt-4")
    assert custom_frame.default_model == "gpt-4"
    assert custom_frame.llm_service.default_model == "gpt-4"


@pytest.mark.asyncio
async def test_create_framer(frame):
    config = FramerConfig(
        name="TestFramer",
        description="A test framer",
        default_model="gpt-3.5-turbo",
    )
    framer = await frame.create_framer(config)
    assert framer.config.name == "TestFramer"
    assert framer.config.description == "A test framer"
    assert framer.config.default_model == "gpt-3.5-turbo"


def test_set_default_model(frame):
    frame.set_default_model("gpt-4")
    assert frame.default_model == "gpt-4"
    assert frame.llm_service.default_model == "gpt-4"


@pytest.mark.asyncio
async def test_get_completion(frame, mocker):
    mock_get_completion = AsyncMock(return_value="Mocked completion")
    mocker.patch.object(frame.llm_service, "get_completion", mock_get_completion)

    result = await frame.get_completion("Test prompt")
    assert isinstance(result, str)
    assert result == "Mocked completion"

    # Check if the mock was called
    assert mock_get_completion.called

    # Get the actual call arguments
    call_args = mock_get_completion.call_args

    # Check if the prompt contains the expected content
    assert "Test prompt" in call_args[0][0]

    # Check the other arguments
    assert call_args[1].get("model", frame.default_model) == "gpt-3.5-turbo"
    # Temperature is not passed in the function call, so it should use the default value
    assert "temperature" not in call_args[1]
    assert call_args[1].get("additional_context") is None
    assert call_args[1].get("expected_output") is None
    assert "use_local" not in call_args[1]  # use_local is not passed to the LLM service
    assert (
        "add_pretext" not in call_args[1]
    )  # This parameter is not passed to the LLM service
    assert call_args[1].get("stream") is False
