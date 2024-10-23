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
    return LLMService(huggingface_api_key="dummy_key")


def test_set_default_model(llm_service):
    initial_model = llm_service.default_model
    new_model = "gpt-4"

    llm_service.set_default_model(new_model)

    assert llm_service.default_model == new_model
    assert llm_service.default_model != initial_model


@pytest.mark.asyncio
async def test_get_completion_huggingface(llm_service):
    async def mock_stream():
        yield "Mock streamed data"

    with patch.object(llm_service, "get_adapter") as mock_get_adapter:
        mock_hf_adapter = AsyncMock()
        mock_hf_adapter.get_completion.return_value = "HuggingFace completion"
        mock_get_adapter.return_value = mock_hf_adapter
        result = await llm_service.get_completion(
            "Test prompt", model="huggingface/gpt2", use_local=True
        )
        assert result == "HuggingFace completion"
        mock_hf_adapter.get_completion.assert_called_once()


@pytest.mark.asyncio
async def test_get_completion_dspy(llm_service):
    with patch.object(llm_service, "get_adapter") as mock_get_adapter:
        mock_dspy_adapter = AsyncMock()
        mock_dspy_adapter.get_completion.return_value = "DSPy completion"
        mock_get_adapter.return_value = mock_dspy_adapter
        result = await llm_service.get_completion("Test prompt", model="dspy-model")
        assert result == "DSPy completion"
        mock_dspy_adapter.get_completion.assert_called_once()


@pytest.mark.asyncio
async def test_get_completion_lmql(llm_service):
    with patch.object(llm_service, "get_adapter") as mock_get_adapter:
        mock_lmql_adapter = AsyncMock()
        mock_lmql_adapter.get_completion.return_value = "LMQL completion"
        mock_get_adapter.return_value = mock_lmql_adapter
        result = await llm_service.get_completion("Test prompt", model="gpt-3.5-turbo")
        assert result == "LMQL completion"
        mock_lmql_adapter.get_completion.assert_called_once()


@pytest.mark.asyncio
async def test_get_completion_with_expected_output(llm_service):
    @patch.object(LLMService, "get_adapter")
    async def test_get_completion_with_stream(mock_get_adapter, llm_service):
        async def mock_stream():
            yield "Streamed "
            yield "completion"

        mock_adapter = MagicMock()
        mock_adapter.get_completion.return_value = mock_stream()
        mock_get_adapter.return_value = mock_adapter

        result = await llm_service.get_completion("Test prompt", stream=True)
        assert hasattr(result, "__aiter__"), "Result is not an async generator"
        streamed_result = ""
        async for chunk in result:
            streamed_result += chunk
        assert streamed_result == "Streamed completion"
        mock_adapter.get_completion.assert_called_once()
