import pytest
from unittest.mock import AsyncMock, patch
from frame.src.services.llm.main import (
    LLMService,
    HuggingFaceConfig,
    DSPyConfig,
    LMQLConfig,
)


@pytest.fixture
def llm_service():
    return LLMService()


def test_set_default_model(llm_service):
    initial_model = llm_service.default_model
    new_model = "gpt-4"

    llm_service.set_default_model(new_model)

    assert llm_service.default_model == new_model
    assert llm_service.default_model != initial_model


@pytest.mark.asyncio
async def test_get_completion_huggingface(llm_service):
    with patch.object(
        llm_service.huggingface_adapter, "get_completion", new_callable=AsyncMock
    ) as mock_hf:
        mock_hf.return_value = "HuggingFace completion"
        result = await llm_service.get_completion(
            "Test prompt", model="huggingface/gpt2", use_local=True
        )
        assert result == "HuggingFace completion"
        mock_hf.assert_called_once()


@pytest.mark.asyncio
async def test_get_completion_dspy(llm_service):
    with patch.object(
        llm_service.dspy_wrapper, "get_completion", new_callable=AsyncMock
    ) as mock_dspy:
        mock_dspy.return_value = "DSPy completion"
        result = await llm_service.get_completion("Test prompt", model="dspy-model")
        assert result == "DSPy completion"
        mock_dspy.assert_called_once()


@pytest.mark.asyncio
async def test_get_completion_lmql(llm_service):
    with patch.object(
        llm_service.lmql_wrapper, "get_completion", new_callable=AsyncMock
    ) as mock_lmql:
        mock_lmql.return_value = "LMQL completion"
        result = await llm_service.get_completion("Test prompt", model="gpt-3.5-turbo")
        assert result == "LMQL completion"
        mock_lmql.assert_called_once()


@pytest.mark.asyncio
async def test_get_completion_with_expected_output(llm_service):
    with patch.object(
        llm_service.lmql_wrapper, "get_completion", new_callable=AsyncMock
    ) as mock_lmql:
        mock_lmql.return_value = mock_stream()
        result = await llm_service.get_completion(
            "Test prompt", expected_output="Expected format"
        )
        assert result == "LMQL completion with expected output"
        mock_lmql.assert_called_once()
        assert "[RESPONSE]\nExpected format" in mock_lmql.call_args[0][0]


@pytest.mark.asyncio
async def test_get_completion_with_stream(llm_service):
    async def mock_stream():
        yield "Streamed "
        yield "completion"

    with patch.object(
        llm_service.lmql_wrapper, "get_completion", new_callable=AsyncMock
    ) as mock_lmql:
        mock_lmql.return_value = mock_stream()
        result = await llm_service.get_completion("Test prompt", stream=True)
        assert hasattr(result, "__aiter__") or hasattr(
            result, "__anext__"
        )  # Check if it's an async generator or async iterator
        streamed_result = ""
        async for chunk in result:
            streamed_result += chunk
        assert streamed_result == "Streamed completion"
