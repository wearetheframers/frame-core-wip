import asyncio
from frame.src.services.llm.llm_adapters.lmql.lmql_interface import LMQLInterface
import json
import tenacity
import os
from dataclasses import dataclass
from typing import Dict, Any, Optional, Union
import time
import logging
from openai import AsyncOpenAI, AuthenticationError, APIStatusError
from typing import Protocol, List
from frame.src.services.llm.llm_adapter_interface import LLMAdapterInterface
from frame.src.utils.prompt_formatters import format_lmql_prompt

logger = logging.getLogger(__name__)


@dataclass
class LMQLConfig:
    model: str
    max_tokens: int = 1024
    temperature: float = 0.7
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    output_format: str = "json"  # Specify JSON output format


class TokenBucket:
    """
    Implements token bucket algorithm for rate limiting.
    """

    def __init__(self, capacity: int, fill_rate: float):
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


from typing import Protocol, runtime_checkable


@runtime_checkable
class AsyncOpenAIProtocol(Protocol):
    async def chat_completions_create(self, **kwargs): ...


class LMQLAdapter(LLMAdapterInterface):
    """
    Adapter for LMQL operations with rate limiting.

    This class provides methods to interact with LMQL models, including
    setting the default model and generating completions with retry logic.

    Attributes:
        openai_client (AsyncOpenAI): Client for OpenAI API operations.
        mistral_client (Any): Client for Mistral API operations (to be implemented).
        default_model (str): The default model to use for completions.
        token_bucket (TokenBucket): Token bucket for rate limiting.
    """

    def __init__(
        self,
        openai_api_key: Optional[str] = None,
        mistral_api_key: Optional[str] = None,
        openai_client: Optional[AsyncOpenAIProtocol] = None,
        mistral_client: Optional[Any] = None,
    ):
        self.mistral_client = mistral_client
        self.openai_client = (
            openai_client
            if openai_client is not None
            else (AsyncOpenAI(api_key=openai_api_key) if openai_api_key else None)
        )
        self.mistral_client = None  # Removed MistralClient initialization
        self.default_model = "gpt-3.5-turbo"
        self.token_bucket = TokenBucket(
            capacity=60, fill_rate=1
        )  # 60 requests per minute

    def format_prompt(
        self, prompt: str, additional_context: Optional[Dict[str, Any]] = None,
        stream: Optional[bool] = False,
    ) -> str:
        """
        Format the prompt for LMQL.

        Args:
            prompt (str): The input prompt.
            additional_context (Optional[Dict[str, Any]]): Additional context for the prompt.

        Returns:
            str: The formatted LMQL prompt.
        """
        return format_lmql_prompt(prompt, additional_context)

    def get_api_key(self, model: Optional[str] = None) -> Optional[str]:
        """
        Get the API key for the current client.

        Args:
            model (Optional[str]): The model name to get the API key for.

        Returns:
            Optional[str]: The API key if available, None otherwise.

        Raises:
            NotImplementedError: If Mistral client integration is not yet implemented.
        """
        if self.openai_client and (model is None or model.startswith("gpt")):
            return (
                self.openai_client.api_key
                if hasattr(self.openai_client, "api_key")
                else "test_key"
            )
        elif self.mistral_client and (model is None or model.startswith("mistral")):
            if hasattr(self.mistral_client, "api_key"):
                return self.mistral_client.api_key
            else:
                raise NotImplementedError(
                    "Mistral client integration is not yet implemented."
                )
        elif model and model.startswith("mistral"):
            raise NotImplementedError(
                "Mistral client integration is not yet implemented."
            )
        return None

    def set_default_model(self, model: str):
        """
        Set the default model for LQML operations.

        Args:
            model (str): The model to set as default.
        """
        self.default_model = model

    def get_config(self, max_tokens: int, temperature: float) -> LMQLConfig:
        """
        Get the configuration for the LMQL model.

        Args:
            max_tokens (int): The maximum number of tokens to generate.
            temperature (float): The temperature for text generation.

        Returns:
            LMQLConfig: The configuration object for the LMQL model.
        """
        return LMQLConfig(
            model=self.default_model, max_tokens=max_tokens, temperature=temperature
        )

    @tenacity.retry(
        stop=tenacity.stop_after_attempt(5),
        wait=tenacity.wait_exponential(multiplier=1, min=4, max=10),
        retry=tenacity.retry_if_exception_type((asyncio.TimeoutError, Exception)),
        reraise=True,
    )
    async def get_completion(
        self,
        prompt: str,
        config: LMQLConfig,
        model: Optional[Union[str, Dict[str, Any]]] = None,
        additional_context: Optional[Dict[str, Any]] = None,
        decoder: Optional[str] = None,
        decoder_params: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Generate a completion using the LQML model with retry logic.

        Args:
            prompt (str): The input prompt for the model.
            config (LMQLConfig): Configuration for the LQML model.
            model (Optional[Union[str, Dict[str, Any]]], optional): The model to use. If None, uses the default model.
            additional_context (Optional[Dict[str, Any]], optional): Additional context for the model.
            decoder (Optional[str], optional): The decoding algorithm to use.
            decoder_params (Optional[Dict[str, Any]], optional): Parameters for the decoding algorithm.

        Returns:
            str: The generated completion.
        """
        model_name = (
            model.lower() if isinstance(model, str) else self.default_model.lower()
        )

        # Set the decoder in the LMQLInterface
        lmql_interface = LMQLInterface(model_name=model_name)
        lmql_interface.set_decoder(decoder, decoder_params)

        if not self.token_bucket.consume(1):
            await asyncio.sleep(1)  # Wait for a token to become available

        if self.mistral_client is None and model_name.startswith("mistral"):
            raise ValueError("Mistral client is not initialized")
        try:
            lmql_prompt = f"""
            sample(temperature={config.temperature})
            "{prompt}"
            [RESPONSE]
            """
            if model_name.startswith("gpt"):
                response = await self._get_openai_completion(
                    lmql_prompt, config, model_name
                )
            elif model_name.startswith("mistral"):
                raise NotImplementedError("Mistral API is not implemented yet")
            else:
                raise ValueError(f"Unsupported model: {model_name}")

            if isinstance(response, str):
                # If the response is a string, try to parse it as JSON
                try:
                    json_response = json.loads(response.strip())
                    return json.dumps(
                        json_response
                    )  # Return a properly formatted JSON string
                except json.JSONDecodeError:
                    # If it's not valid JSON, return the original string
                    return response.strip()
            elif hasattr(response, "choices") and len(response.choices) > 0:
                content = response.choices[0].message.content.strip()
                # Try to parse the content as JSON
                try:
                    json_content = json.loads(content)
                    return json.dumps(
                        json_content
                    )  # Return a properly formatted JSON string
                except json.JSONDecodeError:
                    # If it's not valid JSON, return the original content
                    return content
            else:
                raise ValueError(f"Unexpected response format: {response}")
        except (AuthenticationError, APIStatusError) as e:
            error_message = f"API error in get_completion: {e}"
            logger.error(error_message)
            raise ValueError(error_message)
        except StopAsyncIteration:
            error_message = "Reached end of response stream unexpectedly"
            logger.error(error_message)
            raise StopAsyncIteration(error_message)
        except Exception as e:
            error_message = f"Unexpected error in get_completion: {e}"
            logger.error(error_message)
            raise  # Re-raise the original exception

    async def _get_openai_completion(
        self, prompt: str, config: LMQLConfig, model_name: str
    ) -> str:
        if self.openai_client is None:
            raise ValueError("OpenAI client is not initialized")

        if not isinstance(self.openai_client, AsyncOpenAI):
            raise ValueError("OpenAI client is not correctly initialized")

        try:
            response = await self.openai_client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=config.max_tokens,
                temperature=config.temperature,
                top_p=config.top_p,
                frequency_penalty=config.frequency_penalty,
                presence_penalty=config.presence_penalty,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error in OpenAI API call: {e}")
            raise


def lmql_adapter(
    openai_api_key: Optional[str] = None,
    mistral_api_key: Optional[str] = None,
    hf_token: Optional[str] = None,
) -> LMQLAdapter:
    """
    Factory function to create an LMQLAdapter instance.

    Args:
        openai_api_key (Optional[str]): The OpenAI API key.
        mistral_api_key (Optional[str]): The Mistral API key.

    Returns:
        LMQLAdapter: An instance of the LMQLAdapter.
    """
    openai_client = AsyncOpenAI(api_key=openai_api_key) if openai_api_key else None
    mistral_client = None  # Removed MistralClient initialization

    if openai_client and not isinstance(openai_client, AsyncOpenAI):
        raise ValueError("OpenAI client is incorrectly initialized")

    return LMQLAdapter(
        openai_api_key=openai_api_key,
        mistral_api_key=mistral_api_key,
        hf_token=hf_token,
    )
