from typing import Optional, Dict, Any
from .src.framer.framer import Framer, FramerConfig
from .src.framer.framer_factory import FramerBuilder, FramerFactory
from .src.framed import Framed
from .src.framed.framed_factory import FramedFactory
from .src.constants.models import DEFAULT_MODEL
from .src.framed.framed_factory import FramedBuilder
from .src.framer.config import FramerConfig
from .src.services.llm.main import LLMService
from .src.utils.llm_utils import LLMMetrics, llm_metrics, track_llm_usage
from frame.src.utils.llm_utils import track_llm_usage
from .src.services import ExecutionContextService


class Frame:
    """
    Frame is the main interface for creating and managing Framer instances.

    It acts as the central hub for initializing and orchestrating the various
    components of the Frame framework, including language model services and
    Framer creation.

    The Frame class is responsible for:
    1. Initializing and managing the language model service.
    2. Creating new Framer instances with specified configurations.
    3. Setting and managing the default language model.
    4. Providing a high-level interface for language model completions.

    Attributes:
        _default_model (str): The default language model to use.
        llm_service (LLMService): The language model service instance.
    """

    def reset_metrics(self):
        """Reset the metrics for the Frame instance."""
        self.llm_service.reset_metrics()

    def __init__(
        self,
        openai_api_key: str = "",
        mistral_api_key: str = "",
        huggingface_api_key: str = "",
        default_model: str = DEFAULT_MODEL,
    ):
        """
        Initialize the Frame instance.

        This constructor sets up the Frame with the necessary API keys and
        initializes the language model service. It also sets the default
        model to be used for completions.

        Args:
            openai_api_key (Optional[str]): API key for OpenAI services.
            mistral_api_key (Optional[str]): API key for Mistral services.
            huggingface_api_key (Optional[str]): API key for Hugging Face services.
            default_model (Optional[str]): The default language model to use.
        """
        self._default_model = default_model
        # Initialize the language model service with provided API keys
        self.llm_service = LLMService(
            openai_api_key=openai_api_key,
            mistral_api_key=mistral_api_key,
            huggingface_api_key=huggingface_api_key,
            default_model=self._default_model,
        )

    async def create_framer(self, config: FramerConfig, **kwargs: Any) -> "Framer":
        """
        Create a new Framer instance.

        This method uses the FramerBuilder to construct a new Framer based on
        the provided configuration. It encapsulates the complexity of Framer
        creation and ensures that each Framer is properly initialized with
        the current language model service.

        Args:
            config (FramerConfig): Configuration for the new Framer.
            **kwargs: Additional keyword arguments to pass to the FramerBuilder.

        Returns:
            Framer: A new Framer instance, fully configured and ready to use.
        """
        framer_builder = FramerBuilder(config, self.llm_service)
        return await framer_builder.build()

    def load_framer_from_file(self, file_path: str) -> Framer:
        return Framer.load_from_file(file_path, self.llm_service)

    async def create_framed(self, config: FramerConfig, **kwargs: Any) -> "Framed":
        """
        Create a new Framed instance.

        This method uses the FramedBuilder to construct a new Framed based on
        the provided configuration. It encapsulates the complexity of Framed
        creation and ensures that each Framed is properly initialized with
        the current language model service.

        Args:
            config (FramerConfig): Configuration for the new Framed.
            **kwargs: Additional keyword arguments to pass to the FramedBuilder.

        Returns:
            Framed: A new Framed instance, fully configured and ready to use.
        """
        framed_builder = FramedBuilder(config, self.llm_service, **kwargs)
        return await framed_builder.build()

    @property
    def default_model(self) -> Optional[str]:
        """
        Get the current default model.

        Returns:
            Optional[str]: The name of the current default language model.
        """
        return self._default_model

    def set_default_model(self, model: str):
        """
        Set the default language model.

        This method updates both the Frame instance and the LLMService
        with the new default model. This ensures consistency across
        the entire Frame ecosystem.

        Args:
            model (str): The name of the model to set as default.
        """
        self._default_model = model
        self.llm_service.default_model = model

    async def get_completion(self, prompt: str, **kwargs):
        """
        Get a completion from the language model.

        This method is a high-level wrapper around the LLMService's get_completion
        method. It ensures that all necessary parameters are included and provides
        a consistent interface for getting completions across the Frame framework.

        Args:
            prompt (str): The prompt to send to the language model.
            **kwargs: Additional keyword arguments for the language model.

        Returns:
            The completion result from the language model.

        Note:
            This method always includes the 'stream' parameter with a default
            value of False. This can be overridden by passing 'stream=True'
            in the kwargs.
        """
        # Ensure 'stream' parameter is included with a default value of False
        kwargs.setdefault("stream", False)
        model = kwargs.get("model", self.default_model)
        result = await self.llm_service.get_completion(prompt, **kwargs)

        # Calculate tokens used (you may need to implement this based on your LLM service)
        tokens_used = self.calculate_tokens_used(prompt, str(result))

        track_llm_usage(model, tokens_used)

        return result

    def calculate_tokens_used(self, prompt: str, result: str) -> int:
        # Implement token calculation logic here
        # This is a simple estimation, you may want to use a more accurate method
        return len(prompt.split()) + len(result.split())

    def get_metrics(self) -> Dict[str, Any]:
        """
        Get the current LLM usage metrics.

        Returns:
            A dictionary containing the call count and cost for each model,
            as well as the total calls and total cost.
        """
        return self.llm_service.get_metrics()
