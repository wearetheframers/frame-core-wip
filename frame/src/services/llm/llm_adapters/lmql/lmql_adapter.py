import asyncio
import json
import tenacity
import os
from transformers import AutoTokenizer
from frame.src.constants.api_keys import HUGGINGFACE_API_KEY
from dataclasses import dataclass
from typing import Dict, Any, Optional, Union
import time
import logging
from openai import AsyncOpenAI, AuthenticationError, APIStatusError
import lmql
from typing import Protocol, List
from frame.src.services.llm.llm_adapter_interface import LLMAdapterInterface

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
        hf_token: Optional[str] = None,
    ):
        self.hf_token = hf_token or HUGGINGFACE_API_KEY
        if not self.hf_token:
            logger.warning("Hugging Face token is not set. Some features may not work.")
        self.mistral_client = mistral_client
        self.openai_client = (
            openai_client
            if openai_client is not None
            else (AsyncOpenAI(api_key=openai_api_key) if openai_api_key else None)
        )
        self.mistral_client = (
            MistralClient(api_key=mistral_api_key, hf_token=self.hf_token)
            if mistral_api_key or self.hf_token
            else None
        )
        self.default_model = "gpt-3.5-turbo"
        self.token_bucket = TokenBucket(
            capacity=60, fill_rate=1
        )  # 60 requests per minute

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
    ) -> str:
        """
        Generate a completion using the LQML model with retry logic.

        Args:
            prompt (str): The input prompt for the model.
            config (LMQLConfig): Configuration for the LQML model.
            model (Optional[Union[str, Dict[str, Any]]], optional): The model to use. If None, uses the default model.
            additional_context (Optional[Dict[str, Any]], optional): Additional context for the model.

        Returns:
            str: The generated completion.
        """
        model_name = (
            model.lower() if isinstance(model, str) else self.default_model.lower()
        )

        if not self.token_bucket.consume(1):
            await asyncio.sleep(1)  # Wait for a token to become available

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
                response = await self._get_mistral_completion(
                    lmql_prompt, config, model_name
                )
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

    async def _get_mistral_completion(
        self, prompt: str, config: LMQLConfig, model_name: str
    ) -> str:
        try:
            response = await self.mistral_client.generate_completion(
                prompt=prompt,
                model=model_name,
                max_tokens=config.max_tokens,
                temperature=config.temperature,
                top_p=config.top_p,
                frequency_penalty=config.frequency_penalty,
                presence_penalty=config.presence_penalty,
            )
            return response.strip()
        except Exception as e:
            logger.error(f"Error in Mistral API call: {e}")
            raise

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
    mistral_client = MistralClient(api_key=mistral_api_key) if mistral_api_key else None

    if openai_client and not isinstance(openai_client, AsyncOpenAI):
        raise ValueError("OpenAI client is incorrectly initialized")

    return LMQLAdapter(
        openai_api_key=openai_api_key,
        mistral_api_key=mistral_api_key,
        hf_token=hf_token,
    )


class MistralClient:
    def __init__(self, api_key: Optional[str] = None, hf_token: Optional[str] = None):
        self.hf_token = hf_token
        self.api_key = api_key

    async def generate_completion(
        self,
        prompt: str,
        model: str,
        max_tokens: int,
        temperature: float,
        top_p: float,
        frequency_penalty: float,
        presence_penalty: float,
    ) -> str:
        tokenizer = AutoTokenizer.from_pretrained(
            model, token=self.hf_token, trust_remote_code=True
        )
        model_instance = lmql.model(
            model, tokenizer=tokenizer, token=self.hf_token, trust_remote_code=True
        )
        if not model_instance:
            raise ValueError(
                f"Model {model} could not be loaded. Please check the model identifier and ensure it is available on Hugging Face."
            )
        if asyncio.get_event_loop().is_running():
            response = await model_instance.generate(prompt, max_tokens=max_tokens)
        else:
            response = asyncio.run(
                model_instance.generate(prompt, max_tokens=max_tokens)
            )

        if response:
            return response.strip()
        else:
            raise ValueError("No response from LMQL model")
