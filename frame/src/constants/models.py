# List of available models
AVAILABLE_MODELS = [
    "gpt-3.5-turbo",
    "gpt-4",
    "gpt-4-32k",
    "gpt-4o",
    "mistral-7b-instruct-v0.1",
    "mistral-7b-instruct-v0.2",
    "mistral-medium",
    "mistral-small",
    "mistral-tiny",
    # Add more models as needed
]


def is_model_supported(model: str) -> bool:
    """Check if the given model is supported."""
    return model in AVAILABLE_MODELS
