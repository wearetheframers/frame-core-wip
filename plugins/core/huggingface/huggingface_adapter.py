import asyncio
import tenacity
from dataclasses import dataclass
from typing import Dict, Any, Optional
import time
import logging
from frame.framer.brain.plugins.base import BasePlugin
from frame.src.services.llm.llm_adapter_interface import LLMAdapterInterface

logger = logging.getLogger(__name__)

@dataclass
class HuggingFaceConfig:
    model: str
    max_tokens: int = 1024
    temperature: float = 0.7
    top_p: float = 1.0
    repetition_penalty: float = 1.0

class HuggingFaceAdapter(LLMAdapterInterface):
    """
    Adapter for Hugging Face operations with rate limiting.
    """
    def __init__(self, huggingface_api_key: str):
        self.huggingface_api_key = huggingface_api_key
        self.default_model = "gpt2"
        self.api_key = huggingface_api_key
        self._tokenizer = None
        self._model = None

        # Lazy import transformers only when adapter is used
        try:
            import torch
            from transformers import AutoTokenizer, AutoModelForCausalLM
            self.AutoTokenizer = AutoTokenizer
            self.AutoModelForCausalLM = AutoModelForCausalLM
            self.torch = torch
        except ImportError:
            logger.warning("transformers/torch not installed. Install with: pip install transformers torch")
            self.AutoTokenizer = None
            self.AutoModelForCausalLM = None
            self.torch = None

    def set_default_model(self, model: str):
        self.default_model = model
        self._tokenizer = None
        self._model = None

    def get_config(self, max_tokens: int, temperature: float) -> HuggingFaceConfig:
        return HuggingFaceConfig(
            model=self.default_model,
            max_tokens=max_tokens,
            temperature=temperature
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
        config: HuggingFaceConfig,
        additional_context: Optional[Dict[str, Any]] = None,
        model: Optional[str] = None,
    ) -> str:
        if not all([self.AutoTokenizer, self.AutoModelForCausalLM, self.torch]):
            raise ImportError("transformers/torch not installed. Install plugin requirements first.")

        model_name = model or self.default_model

        try:
            return await self._get_huggingface_completion(prompt, config, model_name)
        except Exception as e:
            logger.error(f"Error in get_completion: {str(e)}")
            raise

    async def _get_huggingface_completion(
        self, prompt: str, config: HuggingFaceConfig, model_name: str
    ) -> str:
        if self._tokenizer is None or self._model is None:
            self._tokenizer = self.AutoTokenizer.from_pretrained(model_name)
            self._model = self.AutoModelForCausalLM.from_pretrained(model_name)

        inputs = self._tokenizer(prompt, return_tensors="pt")
        input_length = inputs["input_ids"].shape[1]
        max_new_tokens = max(config.max_tokens - input_length, 1)

        attention_mask = inputs.get(
            "attention_mask", self.torch.ones_like(inputs["input_ids"])
        )

        outputs = self._model.generate(
            inputs["input_ids"],
            max_new_tokens=max_new_tokens,
            temperature=config.temperature,
            top_p=config.top_p,
            repetition_penalty=config.repetition_penalty,
            do_sample=True,
            pad_token_id=self._tokenizer.eos_token_id,
            attention_mask=attention_mask,
        )

        return self._tokenizer.decode(outputs[0], skip_special_tokens=True)

class HuggingFacePlugin(BasePlugin):
    """Plugin to register HuggingFace adapter with Frame"""
    
    async def on_load(self):
        from frame.src.services.llm.llm_adapters import register_adapter
        register_adapter('huggingface', HuggingFaceAdapter)
