import asyncio
import tenacity
from dataclasses import dataclass
from typing import Dict, Any, Optional
import time
import logging
from transformers import AutoTokenizer, AutoModelForCausalLM
from frame.src.services.llm.llm_adapter_interface import LLMAdapterInterface

logger = logging.getLogger(__name__)


@dataclass
class HuggingFaceConfig:
    model: str
    max_tokens: int = 1024
    temperature: float = 0.7
    top_p: float = 1.0
    repetition_penalty: float = 1.0


class TokenBucket:
    """
    Implements token bucket algorithm for rate limiting.
    """

    def __init__(self, capacity: int, fill_rate: float, api_key: Optional[str] = None):
        self.api_key = api_key
        self.capacity = capacity
        self.fill_rate = fill_rate
        self.tokens = capacity
        self.last_fill = time.time()

    def _fill(self):
        now = time.time()
        delta = now - self.last_fill
        self.tokens = min(self.capacity, self.tokens + delta * self.fill_rate)
        self.last_fill = now

    def consume(self, tokens: int) -> bool:
        self._fill()
        if tokens <= self.tokens:
            self.tokens -= tokens
            return True
        return False


class HuggingFaceAdapter(LLMAdapterInterface):
    """
    Adapter for Hugging Face operations with rate limiting.

    This class provides methods to interact with Hugging Face models, including
    setting the default model and generating completions with retry logic.

    Attributes:
        config (HuggingFaceConfig): Configuration for Hugging Face operations.
        token_bucket (TokenBucket): Token bucket for rate limiting.
    """

    """Adapter for Hugging Face operations with rate limiting."""

    def __init__(self, huggingface_api_key: str):
        self.huggingface_api_key = huggingface_api_key
        self.default_model = "gpt2"
        self.api_key = huggingface_api_key
        self.token_bucket = TokenBucket(
            capacity=60, fill_rate=1
        )  # 60 requests per minute

    def set_default_model(self, model: str):
        """
        Set the default model for Hugging Face operations.

        Args:
            model (str): The model to set as default.
        """
        self.default_model = model

    @tenacity.retry(
        stop=tenacity.stop_after_attempt(5),
        wait=tenacity.wait_exponential(multiplier=1, min=4, max=10),
        retry=tenacity.retry_if_exception_type((asyncio.TimeoutError, Exception)),
        reraise=True,
    )
    async def get_completion(
        self,
        prompt: str,
        config: HuggingFaceConfig,
        additional_context: Optional[Dict[str, Any]] = None,
        model: Optional[str] = None,
    ) -> str:
        """
        Generate a completion using the Hugging Face model with retry logic.

        Args:
            prompt (str): The input prompt for the model.
            config (HuggingFaceConfig): Configuration for the Hugging Face model.
            additional_context (Optional[Dict[str, Any]], optional): Additional context for the model.
            model (Optional[str], optional): The model to use.

        Returns:
            str: The generated completion.
        """
        model_name = model or self.default_model

        if not self.token_bucket.consume(1):
            await asyncio.sleep(1)  # Wait for a token to become available

        try:
            return await self._get_huggingface_completion(prompt, config, model_name)
        except Exception as e:
            logger.error(f"Error in get_completion: {str(e)}")
            raise

    async def _get_huggingface_completion(
        self, prompt: str, config: HuggingFaceConfig, model_name: str
    ) -> str:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)

        inputs = tokenizer(prompt, return_tensors="pt")
        outputs = model.generate(
            inputs["input_ids"],
            max_length=config.max_tokens,
            temperature=config.temperature,
            top_p=config.top_p,
            repetition_penalty=config.repetition_penalty,
            do_sample=True,
        )

        return tokenizer.decode(outputs[0], skip_special_tokens=True)
