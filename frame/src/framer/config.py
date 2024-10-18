from typing import Optional, List, Dict, Any, Union
from frame.src.constants import DEFAULT_MODEL
from pydantic import BaseModel, Field
import logging
from frame.src.constants import HUGGINGFACE_API_KEY, MEM0_API_KEY
from frame.src.utils.log_manager import setup_logging, get_logger


class FramerConfig(BaseModel):
    name: str
    model: Optional[str] = None
    soul_seed: Optional[Union[str, Dict[str, Any]]] = "You are a helpful AI assistant."
    use_local_model: bool = False
    # Default permissions include services like memory, eq, and shared_context.
    # These services do not require explicit permissions to be accessed.
    permissions: Optional[List[str]] = Field(default_factory=lambda: ["with_memory", "with_mem0_search_extract_summarize_plugin", "with_shared_context"])
    mem0_api_key: Optional[str] = MEM0_API_KEY
    """
    Configuration class for Framer instances.

    This class initializes a Framer configuration based on a dictionary of settings.
    It uses the FramerConfigModel to validate and set default values for the configuration.

    Attributes:
        name (str): The name of the Framer.
        description (Optional[str]): The description of the Framer.
        singleton (Optional[bool]): Whether the Framer is a singleton instance.
        gender (Optional[str]): The gender of the Framer.
        default_model (Optional[str]): The default language model to use.
        multi_modal_model (Optional[str]): The multi-modal model to use.
        llm_temperature (Optional[float]): The temperature setting for language model responses.
        llm_max_tokens (Optional[int]): The maximum number of tokens for language model responses.
        llm_top_p (Optional[float]): The top_p setting for language model responses.
        llm_frequency_penalty (Optional[float]): The frequency penalty for language model responses.
        llm_presence_penalty (Optional[float]): The presence penalty for language model responses.
        is_multi_modal (Optional[bool]): Indicates if multi-modal capabilities are enabled.
        roles (Optional[List[Dict[str, str]]]): The roles for the Framer.
        goals (Optional[List[Dict[str, Any]]]): The goals for the Framer.
    """

    description: Optional[str] = None
    singleton: Optional[bool] = False
    gender: Optional[str] = "neutral"
    default_model: Optional[str] = "gpt-4o-mini"
    multi_modal_model: Optional[str] = "gpt-4-vision-preview"
    llm_temperature: Optional[float] = 0.7
    llm_max_tokens: Optional[int] = 1024
    llm_top_p: Optional[float] = 1.0
    llm_frequency_penalty: Optional[float] = 0.0
    llm_presence_penalty: Optional[float] = 0.0
    is_multi_modal: Optional[bool] = False
    roles: Optional[List[Dict[str, Any]]] = None
    goals: Optional[List[Dict[str, Any]]] = None
    recent_memories_limit: Optional[int] = 5

    def __init__(self, **data):
        super().__init__(**data)
        if self.default_model:
            self.default_model = self.default_model.lower()
        if self.use_local_model and not HUGGINGFACE_API_KEY.strip():
            logger = get_logger(__name__)
            logger.error(
                "Error: Hugging Face API key is not set, but the Framer is set to use local models. Some features may not work."
            )
