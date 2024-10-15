import pytest
from frame.src.utils.llm_utils import get_llm_provider


@pytest.mark.parametrize(
    "default_model, use_local, expected_provider",
    [
        ("gpt-3.5-turbo", False, "openai"),
        ("gpt-4", False, "openai"),
        ("mistral-medium", False, "mistral"),
        ("claude-v1", False, "anthropic"),
        ("huggingface-model", False, "huggingface"),
        ("unknown-model", False, "openai"),
        ("gpt-3.5-turbo", True, "huggingface"),
        (None, False, "openai"),
    ],
)
def test_get_llm_provider(default_model, use_local, expected_provider):
    assert get_llm_provider(default_model, use_local) == expected_provider


def test_get_llm_provider_local_model():
    assert get_llm_provider("any-model", True) == "huggingface"


def test_get_llm_provider_default_to_openai():
    assert get_llm_provider("unknown-model", False) == "openai"
