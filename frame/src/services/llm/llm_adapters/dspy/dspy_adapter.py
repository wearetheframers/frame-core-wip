import asyncio
import time
from typing import Dict, Any, Optional, Union, AsyncGenerator, List
import tenacity
from dataclasses import dataclass
import logging
import dspy
from frame.src.services.llm.llm_adapter_interface import LLMAdapterInterface

logger = logging.getLogger(__name__)


class TokenBucket:
    """
    Implements token bucket algorithm for rate limiting.

    This class is used to control the rate of requests to the DSPy service.
    """

    def __init__(self, capacity: int = 60, fill_rate: float = 1.0):
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

    def reset(self):
        self.tokens = self.capacity
        self.last_fill = time.time()

    def get_tokens(self) -> float:
        self._fill()
        return round(self.tokens, 2)


@dataclass
class DSPyConfig:
    model: str
    max_tokens: Optional[int] = None
    temperature: float = 0.7
    supported_models: Optional[List[str]] = None


class DSPyAdapter(LLMAdapterInterface):
    """
    Adapter for DSPy operations with rate limiting.

    This class provides methods to interact with DSPy models, including
    generating completions with retry logic for handling exceptions.

    Attributes:
        config (DSPyConfig): Configuration for DSPy operations.
        token_bucket (TokenBucket): Token bucket for rate limiting.
    """

    def __init__(self, openai_api_key: str):
        self.openai_api_key = openai_api_key
        self.default_model = "gpt-3.5-turbo"
        self.token_bucket = TokenBucket(
            capacity=60, fill_rate=1
        )  # 60 requests per minute
        # Defer configuration to when it's actually needed

    def set_default_model(self, model: str):
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
        config: DSPyConfig,
        additional_context: Optional[Dict[str, Any]] = None,
        model: Optional[str] = None,
        stream: bool = False,
    ) -> Union[str, AsyncGenerator[str, None]]:
        """
        Generate a completion using the DSPy model with retry logic.

        Args:
            prompt (str): The input prompt for the model.
            config (DSPyConfig): Configuration for the DSPy model.
            additional_context (Optional[Dict[str, Any]], optional): Additional context for the model.
            model (Optional[str], optional): The model to use. If None, uses the default model.
            stream (bool, optional): Whether to stream the output. Defaults to False.

        Returns:
            Union[str, AsyncGenerator[str, None]]: The generated completion or a stream of completions.

        Raises:
            ValueError: If streaming is requested, as DSPy does not support it.
        """
        try:
            logger.debug(f"get_completion called with prompt: {prompt}, model: {model}")
            if stream:
                raise ValueError("DSPy does not support streaming mode.")
            tokens_required = await self._get_tokens_required(prompt)

            await self._wait_for_token_bucket(tokens_required)

            model = model or self.default_model
            if config.supported_models and model not in config.supported_models:
                raise ValueError(f"Unsupported model: {model}")

            logger.debug(f"Attempting to get DSPy completion for model: {model}")
            response = await self._get_dspy_completion(prompt, config, model)
            logger.debug(f"Received response: {response}")
            return response.strip()
        except Exception as e:
            logger.error(f"Error in DSPyAdapter.get_completion: {str(e)}")
            raise

    async def _wait_for_token_bucket(self, tokens_required: int):
        while not self.token_bucket.consume(tokens_required):
            await asyncio.sleep(0.1)  # Reduced sleep time

    async def _get_tokens_required(self, prompt: str) -> int:
        # Implement a method to estimate the number of tokens required
        # This is a simple estimation, you might want to use a more accurate method
        return len(prompt.split()) + 20  # Add some buffer for safety

    async def _stream_completion(
        self, prompt: str, config: DSPyConfig, model: str
    ) -> AsyncGenerator[str, None]:
        try:
            async for chunk in await self._get_dspy_completion_stream(
                prompt, config, model
            ):
                yield chunk.strip()
        except Exception as e:
            logger.error(f"Error in DSPyAdapter._stream_completion: {str(e)}")
            raise

    async def _get_dspy_completion_stream(
        self, prompt: str, config: DSPyConfig, model: str
    ) -> AsyncGenerator[str, None]:
        # Implement the actual streaming logic here
        # This is a placeholder implementation
        yield "Streaming "
        yield "response "
        yield "from DSPy"

    async def _get_dspy_completion_stream(
        self, prompt: str, config: DSPyConfig, model_name: str
    ) -> AsyncGenerator[str, None]:
        # class Completion(dspy.Signature):
        #     """Complete the given prompt."""

        #     prompt = dspy.InputField()
        #     completion = dspy.OutputField()

        # lm = dspy.OpenAI(model=model_name)
        # completion_module = dspy.Module(Completion)

        # async for token in completion_module.generate_stream(
        #     prompt=prompt,
        #     config=dspy.Config(
        #         max_tokens=config.max_tokens,
        #         temperature=config.temperature,
        #     ),
        # ):
        #     yield token
        # DSpy does not support streaming mode
        raise ValueError("DSPy does not support streaming mode.")

    async def _get_dspy_completion(
        self, prompt: str, config: DSPyConfig, model_name: str
    ) -> str:
        class Completion(dspy.Signature):
            """Complete the given prompt."""

            prompt = dspy.InputField()
            completion = dspy.OutputField()

        lm = dspy.OpenAI(model=model_name)
        completion_module = dspy.Module(Completion)

        result = await completion_module(
            prompt=prompt,
            config=dspy.Config(
                max_tokens=config.max_tokens,
                temperature=config.temperature,
            ),
        )
        return result.completion

    async def _get_dspy_completion(
        self, prompt: str, config: DSPyConfig, model_name: str
    ) -> str:
        if not hasattr(self, "_lm"):
            self._lm = dspy.OpenAI(api_key=self.openai_api_key)
            dspy.settings.configure(lm=self._lm)
        else:
            self._lm.api_key = self.openai_api_key

        tokens_required = config.max_tokens or 500  # Default to 500 if not set
        if not self.token_bucket.consume(tokens_required):
            await asyncio.sleep(0.1)  # Reduced sleep time

        try:
            result = await asyncio.to_thread(
                self._lm.complete,
                prompt=prompt,
                max_tokens=tokens_required,
                temperature=config.temperature,
            )
            return result.strip()
        except Exception as e:
            logger.error(f"Error in DSPyAdapter._get_dspy_completion: {str(e)}")
            raise
