from frame.src.utils.llm_utils import track_llm_usage
import json
import functools
import logging

logger = logging.getLogger(__name__)


def log_method_call(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"Calling method: {func.__name__}")
        result = func(*args, **kwargs)
        logger.info(f"Method {func.__name__} completed")
        return result

    return wrapper


from frame.src.constants import OPENAI_API_KEY
from .llm_adapters import DSPyAdapter, HuggingFaceAdapter, LMQLAdapter
from frame.src.constants.apis import (
    OPENAI_API_KEY,
    MISTRAL_API_KEY,
    HUGGINGFACE_API_KEY,
)
from frame.src.services.llm.llm_adapters.lmql.lmql_adapter import (
    LMQLAdapter,
    LMQLConfig,
    lmql_adapter,
)
from frame.src.services.llm.llm_adapters.dspy.dspy_adapter import (
    DSPyAdapter,
    DSPyConfig,
)
from frame.src.services.llm.llm_adapters.huggingface.huggingface_adapter import (
    HuggingFaceAdapter,
    HuggingFaceConfig,
)

import logging
import time

from typing import Optional, Dict, Any, Union, AsyncGenerator


from frame.src.utils.llm_utils import llm_metrics, LLMMetrics
from frame.src.utils.prompt_formatters import (
    format_lmql_prompt,
    format_dspy_prompt,
    format_huggingface_prompt,
)


class LLMService:
    """
    LLMService is responsible for managing interactions with various language models.
    It provides methods to set the default model and generate text completions using
    the specified or default model.

    Attributes:
        openai_api_key (str): API key for OpenAI services.
        mistral_api_key (str): API key for Mistral services.
        huggingface_api_key (str): API key for Hugging Face services.
    """

    def __init__(
        self,
        openai_api_key: str = None,
        mistral_api_key: str = None,
        huggingface_api_key: str = None,
        default_model: str = None,
        metrics: LLMMetrics = None,
    ):
        self.logger = logging.getLogger(__name__)
        self.lmql_wrapper = LMQLAdapter(
            openai_api_key=openai_api_key or OPENAI_API_KEY,
            mistral_api_key=mistral_api_key or MISTRAL_API_KEY,
        )
        self.dspy_wrapper = DSPyAdapter(openai_api_key=openai_api_key or OPENAI_API_KEY)
        self.huggingface_adapter = HuggingFaceAdapter(
            huggingface_api_key=huggingface_api_key or HUGGINGFACE_API_KEY
        )
        self.default_model = default_model or (
            "gpt-3.5-turbo" if openai_api_key else "mistral-medium"
        )
        self.metrics = metrics or llm_metrics

    def get_metrics(self) -> Dict[str, Any]:
        """
        Get the current LLM usage metrics.

        Returns:
            Dict[str, Any]: A dictionary containing the call count and cost for each model,
            as well as the total calls and total cost.
        """
        return {
            "models": {
                model: {"calls": data["calls"], "cost": data["cost"]}
                for model, data in self.metrics._metrics["models"].items()
            },
            "total_calls": self.metrics._total_calls,
            "total_cost": self.metrics._total_cost,
        }

    def get_total_calls(self) -> int:
        """
        Get the total number of LLM calls made.

        Returns:
            int: The total number of calls made.
        """
        return self.metrics._total_calls

    def get_total_cost(self) -> float:
        """
        Get the total cost of LLM usage.

        Returns:
            float: The total cost incurred.
        """
        return self.metrics._total_cost

    def set_default_model(self, model: str):
        """
        Set the default model to be used for all operations.

        Args:
            model (str): The model to set as default.
        """
        self.default_model = model
        self.logger.info(f"Default model set to: {self.default_model}")

    async def get_completion(
        self,
        prompt: str,
        model: str = None,
        max_tokens: int = 1024,
        temperature: float = 0.7,
        additional_context: Optional[Dict[str, Any]] = None,
        expected_output: Optional[str] = None,
        use_local: bool = False,
        stream: bool = False,
    ) -> Union[str, Dict[str, Any], AsyncGenerator[str, None]]:
        """
        Generate a completion using the specified model or the default model.

        Args:
            prompt (str): The input prompt for the model.
            model (str, optional): The model to use.
            max_tokens (int, optional): Maximum number of tokens to generate.
            temperature (float, optional): Sampling temperature.
            additional_context (Dict[str, Any], optional): Additional context for the model.
            expected_output (str, optional): Expected output format.
            use_local (bool, optional): Whether to use a local model.
            stream (bool, optional): Whether to stream the output.

        Returns:
            Union[str, Dict[str, Any]]: The generated completion.
        """
        model = model or self.default_model
        self.logger.debug(f"Using model: {model}")

        start_time = time.time()

        if stream:
            self.logger.debug("Streaming mode enabled")
            if "dspy" in model.lower():
                raise ValueError("DSPy does not support streaming mode.")
            elif use_local or (
                self.huggingface_adapter.api_key and "huggingface" in model.lower()
            ):
                self.logger.debug("Using Hugging Face adapter for streaming")
                config = HuggingFaceConfig(
                    model=model, max_tokens=max_tokens, temperature=temperature
                )
                result = self.huggingface_adapter.get_completion(
                    prompt, config, additional_context, stream=True
                )
            elif "mistral" in model.lower():
                self.logger.debug("Using LMQL adapter for Mistral streaming")
                config = LMQLConfig(
                    model=model, max_tokens=max_tokens, temperature=temperature
                )
                lmql_prompt = f'"""{prompt}"""'
                if expected_output:
                    lmql_prompt += f"\n[RESPONSE]\n{expected_output}"
                result = self.lmql_wrapper.get_completion(
                    lmql_prompt, config, additional_context, stream=True
                )
            else:
                self.logger.debug("Using LMQL adapter for OpenAI streaming")
                config = LMQLConfig(
                    model=model, max_tokens=max_tokens, temperature=temperature
                )
                lmql_prompt = f'"""{prompt}"""'
                if expected_output:
                    lmql_prompt += f"\n[RESPONSE]\n{expected_output}"
                result = self.lmql_wrapper.get_completion(
                    lmql_prompt, config, additional_context, stream=True
                )
            
            async def stream_wrapper():
                async for chunk in await result:
                    yield chunk
            return stream_wrapper()
        else:
            if use_local or (
                self.huggingface_adapter.api_key and "huggingface" in model.lower()
            ):
                self.logger.debug("Using Hugging Face adapter")
                config = HuggingFaceConfig(
                    model=model, max_tokens=max_tokens, temperature=temperature
                )
                formatted_prompt = format_huggingface_prompt(prompt)
                result = await self.huggingface_adapter.get_completion(
                    formatted_prompt, config, additional_context
                )
            elif "dspy" in model.lower():
                self.logger.debug("Using DSPy adapter")
                config = DSPyConfig(
                    model=model, max_tokens=max_tokens, temperature=temperature
                )
                formatted_prompt = format_dspy_prompt(prompt)
                result = await self.dspy_wrapper.get_completion(
                    formatted_prompt, config, additional_context
                )
            else:
                self.logger.debug("Using LMQL adapter")
                config = LMQLConfig(
                    model=model, max_tokens=max_tokens, temperature=temperature
                )
                formatted_prompt = format_lmql_prompt(prompt, expected_output)
                result = await self.lmql_wrapper.get_completion(
                    formatted_prompt,
                    config,
                    model=model,
                    additional_context=additional_context,
                )

        end_time = time.time()
        execution_time = end_time - start_time

        # Calculate tokens used (this is a simple estimation)
        if isinstance(result, str):
            tokens_used = len(prompt.split()) + len(result.split())
        else:
            tokens_used = len(
                prompt.split()
            )  # We can't estimate tokens for streaming result

        # Track LLM usage
        track_llm_usage(model, tokens_used)

        self.logger.debug(f"Completion generated in {execution_time:.2f} seconds")
        self.logger.debug(f"Tokens used: {tokens_used}")

        if result is None or (isinstance(result, str) and not result.strip()):
            self.logger.warning(f"Received empty or None response from model: {model}")
            return None

        # Check if ```json is in the response and remove it if present
        if (
            isinstance(result, str)
            and result.startswith("```json")
            and result.endswith("```")
        ):
            try:
                cleaned_response = "\n".join(result.split("\n")[1:-1])
                return cleaned_response
            except json.JSONDecodeError:
                return result

        return result
