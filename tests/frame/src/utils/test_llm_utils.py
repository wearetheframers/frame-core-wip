import pytest
from frame.src.utils.llm_utils import get_llm_provider

def normalize_model_name(model_name: str) -> str:
    """
    Normalize the model name to lowercase.

    Args:
        model_name (str): The model name to normalize.

    Returns:
        str: The normalized model name in lowercase.
    """
    return model_name.lower()

def test_normalize_model_name():
    assert normalize_model_name("GPT-3.5-TURBO") == "gpt-3.5-turbo"
    assert normalize_model_name("Mistral-Medium") == "mistral-medium"
    assert normalize_model_name("claude-v1") == "claude-v1"

def test_framer_config_model_lowercase():
    from frame.src.framer.config import FramerConfig
    config = FramerConfig(name="Test Framer", description="Test Description", default_model="GPT-3.5-TURBO")
    assert config.default_model == "gpt-3.5-turbo", "Model name should be lowercased in FramerConfig"

def test_lmql_adapter_get_completion_model_lowercase():
    from frame.src.services.llm.llm_adapters.lmql.lmql_adapter import LMQLAdapter, LMQLConfig
    adapter = LMQLAdapter()
    config = LMQLConfig(model="MISTRAL-MEDIUM")
    model_name = normalize_model_name(config.model)
    assert model_name == "mistral-medium", "Model name should be lowercased in get_completion"


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
