import pytest
from unittest.mock import MagicMock
from frame.src.utils.llm_utils import get_llm_provider


@pytest.mark.parametrize(
    "use_local_model, default_model, expected_provider",
    [
        (True, "gpt-3.5-turbo", "huggingface"),
        (False, "gpt-3.5-turbo", "openai"),
        (False, "mistral-medium", "mistral"),
        (False, "claude-v1", "anthropic"),
        (False, "unknown-model", "openai"),
    ],
)
def test_get_llm_provider(use_local_model, default_model, expected_provider):
    assert get_llm_provider(use_local_model, default_model) == expected_provider


def test_get_llm_provider_local_model():
    assert get_llm_provider(True, "any-model") == "huggingface"


def test_get_llm_provider_default_to_openai():
    assert get_llm_provider(False, "unknown-model") == "openai"
