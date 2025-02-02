import os
from typing import Dict, Any, Optional
import asyncio
import tenacity
from frame.src.services.llm.llm_adapter_interface import LLMAdapterInterface
from frame.src.services.llm.llm_config import LLMConfig
from .....utils.token_bucket import TokenBucket

class HuggingFaceConfig(LLMConfig):
    """Configuration for HuggingFace operations."""
    model: str = "gpt2"  # Default to GPT-2 as a basic model
    temperature: float = 0.7
    max_tokens: int = 1000
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0

class HuggingFaceAdapter(LLMAdapterInterface):
    """
    Adapter for HuggingFace operations with rate limiting.

    This class provides methods to interact with HuggingFace models, including
    generating completions with retry logic for handling exceptions.

    Attributes:
        config (HuggingFaceConfig): Configuration for HuggingFace operations.
        token_bucket (TokenBucket): Token bucket for rate limiting.
    """

    def __init__(self, huggingface_api_key: str = "", **kwargs):
        """Initialize the HuggingFace adapter with configuration."""
        self.config = HuggingFaceConfig(**kwargs)
        self.token_bucket = TokenBucket(
            tokens=self.config.rate_limit_tokens,
            seconds=self.config.rate_limit_seconds
        )
        self.api_key = huggingface_api_key or os.getenv("HUGGINGFACE_API_KEY", "")

    @tenacity.retry(
        stop=tenacity.stop_after_attempt(5),
        wait=tenacity.wait_exponential(multiplier=1, min=4, max=10),
        retry=tenacity.retry_if_exception_type((asyncio.TimeoutError, Exception)),
        reraise=True,
    )
    async def get_completion(
        self,
        prompt: str,
        config: Optional[HuggingFaceConfig] = None,
        additional_context: Optional[Dict[str, Any]] = None,
        model: Optional[str] = None,
        stream: bool = False,
    ) -> str:
        """
        Get a completion from the HuggingFace model.

        Args:
            prompt: The input prompt for the model.
            config: Optional configuration override.
            additional_context: Additional context for the completion.
            model: Optional model override.
            stream: Whether to stream the response.

        Returns:
            The model's completion response.
        """
        # For now return a mock response
        # TODO: Implement actual HuggingFace integration
        return f"HuggingFace mock response for: {prompt[:30]}..."

    async def close(self):
        """Clean up any resources."""
        pass
