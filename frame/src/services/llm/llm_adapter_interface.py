from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class LLMAdapterInterface(ABC):
    @abstractmethod
    async def get_completion(
        self,
        prompt: str,
        config: Any,
        model: str,
        additional_context: Optional[Dict[str, Any]] = None,
        stream: bool = False,
    ) -> str:
        """
        Get a completion from the language model.

        Note: Streaming mode is not supported by this interface.
        """
        if stream:
            raise ValueError("DSPy does not support streaming mode.")
