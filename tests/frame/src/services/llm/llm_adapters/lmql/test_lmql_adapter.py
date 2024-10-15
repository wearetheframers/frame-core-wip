import pytest
from unittest.mock import AsyncMock, patch
from frame.src.services.llm.llm_adapters.lmql.lmql_adapter import (
    LMQLAdapter,
    LMQLConfig,
)


from openai import AsyncOpenAI


@pytest.fixture
def mock_openai_client():
    mock_client = AsyncMock(spec=AsyncOpenAI)
    mock_client.chat = AsyncMock()
    mock_client.chat.completions = AsyncMock()
    mock_client.chat.completions.create = AsyncMock()
    return mock_client


@pytest.fixture
def lmql_adapter(mock_openai_client):
    return LMQLAdapter(openai_client=mock_openai_client)


@pytest.mark.asyncio
async def test_get_api_key(lmql_adapter):
    # Test with OpenAI client
    api_key = lmql_adapter.get_api_key("gpt-3.5-turbo")
    assert api_key == "test_key"

    # Test with Mistral client (not implemented yet)
    with pytest.raises(NotImplementedError):
        lmql_adapter.get_api_key("mistral-medium")

    # Test with unknown model
    assert lmql_adapter.get_api_key("unknown-model") is None


@pytest.mark.asyncio
async def test_get_completion(lmql_adapter, mock_openai_client):
    config = LMQLConfig(model="gpt-3.5-turbo")
    mock_openai_client.chat.completions.create.return_value.choices[
        0
    ].message.content = "Test completion"

    result = await lmql_adapter.get_completion("Test prompt", config)
    assert result == "Test completion"

    mock_openai_client.chat.completions.create.assert_called_once()


@pytest.mark.asyncio
async def test_get_completion_mistral(lmql_adapter):
    config = LMQLConfig(model="mistral-medium")

    with pytest.raises(ValueError, match="Mistral client is not initialized"):
        await lmql_adapter.get_completion("Test prompt", config, model="mistral-medium")


@pytest.mark.asyncio
async def test_get_completion_unsupported_model(lmql_adapter):
    config = LMQLConfig(model="unsupported-model")

    with pytest.raises(ValueError, match="Unsupported model: unsupported-model"):
        await lmql_adapter.get_completion(
            "Test prompt", config, model="unsupported-model"
        )


@pytest.mark.asyncio
async def test_rate_limiting(lmql_adapter, mock_openai_client):
    config = LMQLConfig(model="gpt-3.5-turbo")
    mock_openai_client.chat.completions.create.return_value = AsyncMock(
        choices=[AsyncMock(message=AsyncMock(content="Test completion"))]
    )

    # Simulate rate limiting
    with patch(
        "frame.src.services.llm.llm_adapters.lmql.lmql_adapter.TokenBucket.consume",
        return_value=False,
    ):
        with patch("asyncio.sleep") as mock_sleep:
            result = await lmql_adapter.get_completion("Test prompt", config)
            mock_sleep.assert_called_once_with(1)

    assert result == "Test completion"
    mock_openai_client.chat.completions.create.assert_called_once()


@pytest.mark.asyncio
async def test_retry_logic(lmql_adapter, mock_openai_client):
    config = LMQLConfig(model="gpt-3.5-turbo")

    # Mock the _get_openai_completion method
    lmql_adapter._get_openai_completion = AsyncMock()
    lmql_adapter._get_openai_completion.side_effect = [
        Exception("API Error"),
        Exception("API Error"),
        AsyncMock(choices=[AsyncMock(message=AsyncMock(content="Test completion"))]),
    ]

    result = await lmql_adapter.get_completion("Test prompt", config)
    assert result == "Test completion"
    assert lmql_adapter._get_openai_completion.call_count == 3

    # Test for retries
    lmql_adapter._get_openai_completion.side_effect = [
        Exception("Reached end of response stream unexpectedly")
    ] * 2
    with pytest.raises(Exception, match="Reached end of response stream unexpectedly"):
        await lmql_adapter.get_completion("Test prompt", config)
    assert (
        lmql_adapter._get_openai_completion.call_count == 8
    )  # 3 from previous + 5 new calls

    # Test for StopAsyncIteration
    lmql_adapter._get_openai_completion.side_effect = StopAsyncIteration(
        "Reached end of response stream unexpectedly"
    )
    with pytest.raises(
        StopAsyncIteration, match="Reached end of response stream unexpectedly"
    ):
        await lmql_adapter.get_completion("Test prompt", config)

    # Reset side_effect for future tests
    lmql_adapter._get_openai_completion.side_effect = None
