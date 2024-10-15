from typing import Dict, Any, Union
from collections import defaultdict
import logging


class LLMMetrics:
    def __init__(self):
        self._metrics: Dict[str, Dict[str, Union[int, float]]] = defaultdict(lambda: {"calls": 0, "cost": 0.0})
        self._total_calls: int = 0
        self._total_cost: float = 0.0

    def increment_call(self, model: str):
        self._metrics[model]["calls"] += 1
        self._total_calls += 1

    def add_cost(self, model: str, cost: float):
        self._metrics[model]["cost"] += cost
        self._total_cost += cost

    def get_total_calls(self) -> int:
        return self._total_calls

    def get_total_cost(self) -> float:
        return self._total_cost

    def get_metrics(self) -> Dict[str, Any]:
        return {
            "models": dict(self._metrics),
            "total_calls": self._total_calls,
            "total_cost": self._total_cost,
        }


llm_metrics = LLMMetrics()


def get_llm_provider(default_model: str, use_local: bool = False) -> str:
    if use_local:
        return "huggingface"
    if default_model is None:
        return "openai"  # Default to OpenAI if no model is specified
    default_model_lower = default_model.lower()
    if "gpt" in default_model_lower:
        return "openai"
    elif "mistral" in default_model_lower:
        return "mistral"
    elif "claude" in default_model_lower:
        return "anthropic"
    elif "huggingface" in default_model_lower:
        return "huggingface"
    else:
        return "openai"  # Default to OpenAI if unknown


def calculate_token_size(text: str) -> int:
    """
    Calculate the number of tokens in a given text.

    Args:
        text (str): The text to calculate tokens for.

    Returns:
        int: The number of tokens in the text.
    """
    return len(text.split())


def choose_best_model_for_tokens(token_count: int) -> str:
    """
    Choose the best model based on the token count.

    Args:
        token_count (int): The number of tokens.

    Returns:
        str: The best model to handle the token size.
    """
    if token_count <= 1000:
        return "gpt-3.5-turbo"
    elif token_count <= 2000:
        return "gpt-3.5-turbo-16k"
    elif token_count <= 4000:
        return "gpt-4"
    else:
        return "gpt-4-32k"


def track_llm_usage(model: str, tokens_used: int):
    llm_metrics.increment_call(model)
    cost = calculate_cost(model, tokens_used)
    llm_metrics.add_cost(model, cost)
    logging.info(f"LLM Usage: Model: {model}, Tokens: {tokens_used}, Cost: ${cost:.4f}")


def calculate_cost(model: str, tokens_used: int) -> float:
    # Define cost per 1000 tokens for each model
    cost_per_1k_tokens = {
        # OpenAI models
        "gpt-3.5-turbo": 0.002,
        "gpt-3.5-turbo-16k": 0.004,
        "gpt-4": 0.03,
        "gpt-4-32k": 0.06,
        "gpt-4-1106-preview": 0.01,
        "gpt-4-1106-vision-preview": 0.01,
        # Anthropic models
        "claude-2": 0.01,
        "claude-instant-1": 0.0015,
        # Mistral models
        "mistral-tiny": 0.00014,
        "mistral-small": 0.0006,
        "mistral-medium": 0.0025,
        "mistral-large": 0.008,
        # Cohere models
        "command": 0.015,
        "command-light": 0.003,
        # AI21 models
        "j2-ultra": 0.016,
        "j2-mid": 0.008,
        # Google models
        "palm-2": 0.0005,
        # Hugging Face models
        "huggingface-default": 0.0001,
        # Meta models
        "llama-2-70b": 0.0007,
        "llama-2-13b": 0.0004,
        "llama-2-7b": 0.0002,
    }

    if model not in cost_per_1k_tokens:
        # Use a default cost if the model is not found
        return (tokens_used / 1000) * 0.001  # Default to $0.001 per 1000 tokens

    return (tokens_used / 1000) * cost_per_1k_tokens[model]


def get_completion(llm_service, prompt: str, model: str = None, **kwargs) -> str:
    """
    Utility function to get a completion from the LLMService.

    Args:
        llm_service (LLMService): The LLMService instance to use.
        prompt (str): The prompt to send to the language model.
        model (str, optional): The model to use for completion.
        **kwargs: Additional keyword arguments for the language model.

    Returns:
        str: The completion result from the language model.
    """
    return llm_service.get_completion(prompt, model=model, **kwargs)
