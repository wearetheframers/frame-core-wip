import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from frame.src.services.llm.llm_adapters.huggingface.huggingface_adapter import (
    HuggingFaceAdapter,
    HuggingFaceConfig,
    TokenBucket,
)


@pytest.fixture
def huggingface_adapter():
    return HuggingFaceAdapter("fake_api_key")


def test_huggingface_adapter_initialization(huggingface_adapter):
    assert isinstance(huggingface_adapter, HuggingFaceAdapter)
    assert huggingface_adapter.huggingface_api_key == "fake_api_key"
    assert huggingface_adapter.default_model == "gpt2"
    assert isinstance(huggingface_adapter.token_bucket, TokenBucket)


def test_set_default_model(huggingface_adapter):
    huggingface_adapter.set_default_model("bert-base-uncased")
    assert huggingface_adapter.default_model == "bert-base-uncased"


@pytest.mark.asyncio
async def test_get_completion(huggingface_adapter):
    config = HuggingFaceConfig(model="gpt2")
    with patch.object(
        huggingface_adapter, "_get_huggingface_completion", new_callable=AsyncMock
    ) as mock_completion:
        mock_completion.return_value = "Test completion"
        result = await huggingface_adapter.get_completion("Test prompt", config)
        assert result == "Test completion"
        mock_completion.assert_called_once_with("Test prompt", config, "gpt2")


def test_token_bucket():
    bucket = TokenBucket(capacity=10, fill_rate=1)
    assert bucket.consume(5)
    assert not bucket.consume(6)
    assert bucket.consume(5)
