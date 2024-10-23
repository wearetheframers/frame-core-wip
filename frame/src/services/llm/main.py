from frame.src.utils.llm_utils import track_llm_usage
from frame.src.services.llm.llm_adapters.lmql.lmql_interface import LMQLInterface
from frame.src.services.llm.llm_adapters.dspy.dspy_adapter import DSPyAdapter
import json
import functools
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)


def clean_response(response: str) -> str:
    """
    Clean the response by removing unwanted text patterns.

    Args:
        response (str): The raw response from the language model.

    Returns:
        str: The cleaned response.
    """
    unwanted_patterns = ["Response:\n", "[RESPONSE]"]
    for pattern in unwanted_patterns:
        response = response.replace(pattern, "")
    return response.strip()


def log_method_call(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"Calling method: {func.__name__}")
        result = func(*args, **kwargs)
        logger.info(f"Method {func.__name__} completed")
        # Clean the response using the LMQL interface
        result = clean_response(result)

        return result

    return wrapper


from frame.src.constants import OPENAI_API_KEY
from .llm_adapters import DSPyAdapter, HuggingFaceAdapter, LMQLAdapter
from frame.src.constants.api_keys import (
    OPENAI_API_KEY,
    MISTRAL_API_KEY,
    HUGGINGFACE_API_KEY,
)
from frame.src.services.llm.llm_adapters.lmql.lmql_adapter import (
    LMQLConfig,
    lmql_adapter,
)
from frame.src.services.llm.llm_adapters.dspy.dspy_adapter import DSPyConfig
from frame.src.services.llm.llm_adapters.huggingface.huggingface_adapter import (
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
        self.openai_api_key = openai_api_key or OPENAI_API_KEY
        self.mistral_api_key = mistral_api_key
        self.huggingface_api_key = huggingface_api_key or HUGGINGFACE_API_KEY
        self.default_model = default_model or (
            "gpt-3.5-turbo" if self.openai_api_key else "mistral-medium"
        )
        self.metrics = metrics or llm_metrics
        self._adapters = {}
        self.huggingface_adapter = HuggingFaceAdapter(huggingface_api_key=self.huggingface_api_key)
        self.dspy_wrapper = DSPyAdapter(openai_api_key=self.openai_api_key)
        self.lmql_wrapper = LMQLAdapter(openai_api_key=self.openai_api_key)

    def get_adapter(self, model_name: str):
        if model_name not in self._adapters:
            if "gpt" in model_name.lower():
                self._adapters[model_name] = LMQLAdapter(
                    openai_api_key=self.openai_api_key
                )
            elif "mistral" in model_name.lower():
                self._adapters[model_name] = LMQLAdapter(
                    mistral_api_key=self.mistral_api_key
                )
            elif "huggingface" in model_name.lower():
                self._adapters[model_name] = HuggingFaceAdapter(
                    huggingface_api_key=self.huggingface_api_key
                )
            elif "dspy" in model_name.lower():
                self._adapters[model_name] = DSPyAdapter(
                    openai_api_key=self.openai_api_key
                )
                raise ValueError(f"Unsupported model: {model_name}")
        return self._adapters[model_name]

    def get_metrics(self) -> Dict[str, Any]:
        """
        Get the current LLM usage metrics.

        Returns:
            Dict[str, Any]: A dictionary containing the call count and cost for each model,
            as well as the total calls and total cost.
        """
        return self.metrics.get_metrics()

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

    def _prepare_full_prompt(
        self,
        prompt: str,
        include_frame_context: bool,
        recent_memories: Optional[List[Dict[str, Any]]],
    ) -> str:
        full_prompt = prompt

        if include_frame_context:
            frame_context = """
            Frame is a multi-modal cognitive agent framework designed to support fully emergent characteristics.
            It consists of three main components: Frame, Framed, and Framer.
            - Frame: The main interface for creating and managing Framer instances.
            - Framer: An individual AI agent with capabilities for task management, decision-making, and interaction with language models.
            - Framed: A collection of Framer objects working together to achieve complex tasks.
            """
            full_prompt = f"{frame_context}\n\n{full_prompt}"

        if recent_memories:
            memories_context = "Recent memories and perceptions:\n"
            for memory in recent_memories:
                memories_context += (
                    f"- {memory.get('type', 'Memory')}: {memory.get('content', '')}\n"
                )
            full_prompt = f"{memories_context}\n{full_prompt}"

        return full_prompt

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
        include_frame_context: bool = False,
        recent_memories: Optional[List[Dict[str, Any]]] = None,
    ) -> str:
        model = model or self.default_model
        self.logger.debug(f"Using model: {model}")

        start_time = time.time()

        full_prompt = self._prepare_full_prompt(
            prompt, include_frame_context, recent_memories
        )

        try:
            adapter = self.get_adapter(model)
            config = adapter.get_config(max_tokens=max_tokens, temperature=temperature)
            formatted_prompt = adapter.format_prompt(full_prompt)
            if stream:
                result = adapter.get_completion(formatted_prompt, config, additional_context, stream=True)
                return result  # Return the async generator
            else:
                result = await adapter.get_completion(formatted_prompt, config, additional_context)

            end_time = time.time()
            execution_time = end_time - start_time
            tokens_used = len(full_prompt.split()) + (
                len(result.split()) if isinstance(result, str) else 0
            )

            self.metrics.track_usage(model, tokens_used)

            self.logger.debug(f"Completion generated in {execution_time:.2f} seconds")
            self.logger.debug(f"Tokens used: {tokens_used}")

            if isinstance(result, dict):
                return json.dumps(result)
            elif isinstance(result, str):
                return result
            else:
                return str(result)

        except Exception as e:
            self.logger.error(f"Error in get_completion: {str(e)}")
            return f"I encountered an error while processing your request: {str(e)}. Could you please try again?"
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
            include_frame_context (bool, optional): Whether to include context about Frame and Framers.
            recent_memories (List[Dict[str, Any]], optional): List of recent memories/perceptions.

        Returns:
            Union[str, Dict[str, Any]]: The generated completion.
        """
        model = model or self.default_model
        self.logger.debug(f"Using model: {model}")

        start_time = time.time()

        # Prepare the full prompt with additional context if required
        full_prompt = self._prepare_full_prompt(
            prompt, include_frame_context, recent_memories
        )

        result = None  # Initialize result to avoid UnboundLocalError

        try:
            if stream:
                # ... (streaming code remains unchanged)
                pass
            else:
                if use_local or (
                    self.huggingface_adapter.api_key and "huggingface" in model.lower()
                ):
                    self.logger.debug("Using Hugging Face adapter")
                    config = HuggingFaceConfig(
                        model=model, max_tokens=max_tokens, temperature=temperature
                    )
                    formatted_prompt = format_huggingface_prompt(full_prompt)
                    result = await self.huggingface_adapter.get_completion(
                        formatted_prompt, config, additional_context
                    )
                elif "dspy" in model.lower():
                    self.logger.debug("Using DSPy adapter")
                    config = DSPyConfig(
                        model=model, max_tokens=max_tokens, temperature=temperature
                    )
                    formatted_prompt = format_dspy_prompt(full_prompt)
                    result = await self.dspy_wrapper.get_completion(
                        formatted_prompt, config, additional_context
                    )
                else:
                    self.logger.debug("Using LMQL adapter")
                    config = LMQLConfig(
                        model=model, max_tokens=max_tokens, temperature=temperature
                    )
                    constraints = (
                        [f"EXPECTED_OUTPUT in [{expected_output}]"]
                        if expected_output
                        else []
                    )
                    if "lmql" in model.lower():
                        result = await self.lmql_interface.generate(
                            full_prompt, max_tokens=max_tokens, constraints=constraints
                        )
                    elif "dspy" in model.lower():
                        config = DSPyConfig(
                            model=model, max_tokens=max_tokens, temperature=temperature
                        )
                        formatted_prompt = format_dspy_prompt(full_prompt)
                        result = await self.dspy_wrapper.get_completion(
                            formatted_prompt, config, additional_context
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

            if (
                result is None
                or (isinstance(result, str) and not result.strip())
                or (isinstance(result, dict) and "error" in result)
            ):
                self.logger.warning(f"Received invalid response from model: {model}")
                return {
                    "error": f"Invalid response from model: {model}",
                    "fallback_response": "I apologize, but I couldn't generate a response at this time. Could you please rephrase your question or provide more context?",
                }

            if isinstance(result, dict):
                return result
            elif isinstance(result, str):
                try:
                    return json.loads(result)
                except json.JSONDecodeError:
                    return {"response": result}

            # Check if ```json is in the response and remove it if present
            if (
                isinstance(result, str)
                and result.startswith("```json")
                and result.endswith("```")
            ):
                try:
                    cleaned_response = "\n".join(result.split("\n")[1:-1])
                    return json.loads(cleaned_response)
                except json.JSONDecodeError:
                    return result

            return result

        except Exception as e:
            self.logger.error(f"Error in get_completion: {str(e)}")
            return {
                "error": str(e),
                "fallback_response": "I encountered an error while processing your request. Could you please try again?",
            }
