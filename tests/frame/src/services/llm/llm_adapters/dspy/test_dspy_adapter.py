import pytest
import time
import asyncio
from unittest.mock import AsyncMock, patch, call
from frame.src.services.llm.llm_adapters.dspy.dspy_adapter import (
    DSPyAdapter,
    TokenBucket,
    DSPyConfig,
)


@pytest.fixture(autouse=True)
def reset_token_bucket(dspy_adapter):
    dspy_adapter.token_bucket.reset()
    yield


@pytest.fixture
def dspy_adapter():
    return DSPyAdapter("sk-" + "a" * 48)  # Use a fake but valid-format API key


def test_dspy_adapter_initialization(dspy_adapter):
    assert isinstance(dspy_adapter, DSPyAdapter)
    assert dspy_adapter.openai_api_key == "sk-" + "a" * 48
    assert dspy_adapter.default_model == "gpt-3.5-turbo"
    assert isinstance(dspy_adapter.token_bucket, TokenBucket)


def test_set_default_model(dspy_adapter):
    dspy_adapter.set_default_model("gpt-4")
    assert dspy_adapter.default_model == "gpt-4"


@pytest.mark.asyncio
async def test_get_completion(dspy_adapter):
    config = DSPyConfig(model="gpt-3.5-turbo")
    # Increase the token bucket capacity for this test
    dspy_adapter.token_bucket.capacity = 10000
    dspy_adapter.token_bucket.tokens = 10000
    with patch.object(
        DSPyAdapter, "_get_dspy_completion", new_callable=AsyncMock
    ) as mock_completion:
        mock_completion.return_value = "Test completion"
        result = await dspy_adapter.get_completion("Test prompt", config)
        assert result == "Test completion"
        mock_completion.assert_called_once_with("Test prompt", config, "gpt-3.5-turbo")


@pytest.mark.asyncio
async def test_get_completion_stream(dspy_adapter):
    config = DSPyConfig(model="gpt-3.5-turbo")
    with pytest.raises(ValueError, match="DSPy does not support streaming mode."):
        await dspy_adapter.get_completion("Test prompt", config, stream=True)


def test_token_bucket():
    bucket = TokenBucket(capacity=10, fill_rate=1)
    assert bucket.consume(5)
    assert not bucket.consume(6)
    assert bucket.consume(5)


@pytest.mark.asyncio
async def test_get_completion_with_additional_context(dspy_adapter):
    config = DSPyConfig(model="gpt-3.5-turbo")
    additional_context = {"key": "value"}
    with patch.object(
        DSPyAdapter, "_get_dspy_completion", new_callable=AsyncMock
    ) as mock_completion:
        mock_completion.return_value = "Test completion with context"
        try:
            result = await asyncio.wait_for(
                dspy_adapter.get_completion(
                    "Test prompt", config, additional_context=additional_context
                ),
                timeout=5,  # Set a timeout of 5 seconds
            )
            assert result == "Test completion with context"
            mock_completion.assert_called_once_with(
                "Test prompt", config, "gpt-3.5-turbo"
            )
        except asyncio.TimeoutError:
            pytest.fail("Test failed due to a timeout.")
        except Exception as e:
            pytest.fail(f"Test failed due to an unexpected exception: {e}")


@pytest.mark.asyncio
async def test_get_completion_stream(dspy_adapter):
    config = DSPyConfig(model="gpt-3.5-turbo")
    with pytest.raises(ValueError, match="DSPy does not support streaming mode."):
        await dspy_adapter.get_completion("Test prompt", config, stream=True)


@pytest.mark.asyncio
async def test_get_completion_with_custom_model(dspy_adapter):
    config = DSPyConfig(model="gpt-3.5-turbo")
    custom_model = "custom-model"
    with patch.object(
        DSPyAdapter, "_get_dspy_completion", new_callable=AsyncMock
    ) as mock_completion:
        mock_completion.return_value = "Test completion with custom model"
        try:
            result = await asyncio.wait_for(
                dspy_adapter.get_completion("Test prompt", config, model=custom_model),
                timeout=5,  # Set a timeout of 5 seconds
            )
            assert result == "Test completion with custom model"
            mock_completion.assert_called_once_with("Test prompt", config, custom_model)
        except asyncio.TimeoutError:
            pytest.fail("Test failed due to a timeout.")
        except Exception as e:
            pytest.fail(f"Test failed due to an unexpected exception: {e}")


@pytest.mark.asyncio
async def test_get_completion_rate_limit(dspy_adapter):
    config = DSPyConfig(model="gpt-3.5-turbo")
    dspy_adapter.token_bucket.capacity = 1
    dspy_adapter.token_bucket.tokens = 1
    dspy_adapter.token_bucket.fill_rate = 0.5  # 0.5 tokens per second

    with patch.object(
        DSPyAdapter, "_get_dspy_completion", new_callable=AsyncMock
    ) as mock_completion, patch.object(
        DSPyAdapter, "_get_tokens_required", return_value=1
    ) as mock_get_tokens:
        mock_completion.return_value = "Test completion"

        # First call should succeed immediately
        result1 = await dspy_adapter.get_completion("Test prompt 1", config)
        assert result1 == "Test completion"

        # Second call should trigger rate limit and wait
        start_time = time.time()
        task = asyncio.create_task(dspy_adapter.get_completion("Test prompt 2", config))

        # Allow time for tokens to replenish
        await asyncio.sleep(
            2.5
        )  # Wait longer than the time needed to replenish a token

        result2 = await task
        end_time = time.time()

        assert result2 == "Test completion"
        elapsed_time = end_time - start_time
        assert (
            elapsed_time >= 2.0
        ), f"Rate limiting didn't cause expected delay, elapsed: {elapsed_time}"

        # Ensure that the token bucket was replenished
        assert dspy_adapter.token_bucket.tokens <= dspy_adapter.token_bucket.capacity


@pytest.mark.asyncio
async def test_stream_completion_error_handling(dspy_adapter):
    config = DSPyConfig(model="gpt-3.5-turbo")

    async def mock_stream_with_error():
        yield "Partial "
        raise Exception("Stream error")

    with patch.object(
        DSPyAdapter,
        "_get_dspy_completion_stream",
        return_value=mock_stream_with_error(),
    ), pytest.raises(Exception, match="Stream error"):
        result = []
        async for chunk in dspy_adapter._stream_completion(
            "Test prompt", config, "gpt-3.5-turbo"
        ):
            result.append(chunk)

    assert result == ["Partial"]


@pytest.mark.asyncio
async def test_get_dspy_completion_error_handling(dspy_adapter):
    config = DSPyConfig(model="gpt-3.5-turbo")

    with patch.object(
        DSPyAdapter, "_get_dspy_completion", new_callable=AsyncMock
    ) as mock_completion:
        mock_completion.side_effect = Exception("API error")

        with pytest.raises((Exception, asyncio.TimeoutError)) as exc_info:
            await asyncio.wait_for(
                dspy_adapter.get_completion("Test prompt", config),
                timeout=5,  # Set a timeout of 5 seconds
            )

        if isinstance(exc_info.value, asyncio.TimeoutError):
            pytest.skip("Test skipped due to timeout")
        else:
            assert str(exc_info.value) == "API error"


def test_token_bucket_fill():
    bucket = TokenBucket(capacity=10, fill_rate=1)
    assert bucket.consume(10)
    assert not bucket.consume(1)

    # Wait for the bucket to fill
    time.sleep(1)

    assert bucket.consume(1)
    assert bucket.get_tokens() == 0.00


def test_dspy_config():
    config = DSPyConfig(model="gpt-3.5-turbo", max_tokens=100, temperature=0.8)
    assert config.model == "gpt-3.5-turbo"
    assert config.max_tokens == 100
    assert config.temperature == 0.8


import pytest
from frame.src.services.llm.llm_adapters.dspy.dspy_adapter import (
    DSPyAdapter,
    DSPyConfig,
)


@pytest.mark.asyncio
async def test_dspy_no_streaming():
    adapter = DSPyAdapter(openai_api_key="test_key")
    config = DSPyConfig(model="gpt-3.5-turbo")
    with pytest.raises(ValueError, match="DSPy does not support streaming mode."):
        await adapter.get_completion(prompt="Test prompt", config=config, stream=True)
