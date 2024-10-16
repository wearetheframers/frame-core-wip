import pytest
from unittest.mock import AsyncMock, patch
from frame.src.services.llm.llm_adapters.lmql.lmql_adapter import LMQLAdapter, LMQLConfig

@pytest.fixture
def mock_mistral_client(mocker):
    client = mocker.AsyncMock()
    client.generate_completion.return_value = "Mistral response"
    return client

@pytest.fixture
def lmql_adapter(mock_mistral_client):
    return LMQLAdapter(mistral_api_key="test_key", openai_client=None, mistral_client=mock_mistral_client)

@pytest.mark.asyncio
async def test_mistral_completion(lmql_adapter):
    config = LMQLConfig(model="mistral-model")
    prompt = "Test prompt"
    response = await lmql_adapter.get_completion(prompt, config, model="mistral-model")
    assert response == "Mistral response"
    lmql_adapter.mistral_client.generate_completion.assert_called_once_with(
        prompt=prompt,
        model="mistral-model",
        max_tokens=config.max_tokens,
        temperature=config.temperature,
        top_p=config.top_p,
        frequency_penalty=config.frequency_penalty,
        presence_penalty=config.presence_penalty,
    )
