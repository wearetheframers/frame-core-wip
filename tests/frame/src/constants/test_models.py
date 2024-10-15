import pytest
from frame.src.constants.models import AVAILABLE_MODELS, is_model_supported


def test_available_models():
    assert isinstance(AVAILABLE_MODELS, list)
    assert len(AVAILABLE_MODELS) > 0
    assert all(isinstance(model, str) for model in AVAILABLE_MODELS)


@pytest.mark.parametrize(
    "model,expected",
    [
        ("gpt-3.5-turbo", True),
        ("gpt-4", True),
        ("gpt-4-32k", True),
        ("gpt-4o", True),
        ("mistral-7b-instruct-v0.1", True),
        ("mistral-7b-instruct-v0.2", True),
        ("mistral-medium", True),
        ("mistral-small", True),
        ("mistral-tiny", True),
        ("unsupported-model", False),
    ],
)
def test_is_model_supported(model, expected):
    assert is_model_supported(model) == expected
