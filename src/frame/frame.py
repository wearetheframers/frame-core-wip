import os
import logging
from typing import Optional, Dict, Any
from .src.framer.framer import Framer, FramerConfig
from .src.framer.framer_factory import FramerBuilder, FramerFactory
from .src.framed import Framed

logger = logging.getLogger(__name__)
from .src.framed.framed_factory import FramedFactory
from .src.constants.models import DEFAULT_MODEL
from .src.framed.framed_factory import FramedBuilder
from .src.framer.config import FramerConfig
from .src.services.llm import LLMService
from .src.utils.llm_utils import LLMMetrics, llm_metrics, track_llm_usage
from .src.utils.plugin_loader import load_plugins
from .src.services.context.execution_context_service import ExecutionContext
from .src.utils.plugin_loader import load_plugins


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
    5. Loading and managing plugins.

    Attributes:
        _default_model (str): The default language model to use.
        llm_service (LLMService): The language model service instance.
        plugins_dir (str): The directory containing plugins.
        plugins (Dict[str, Any]): Loaded plugins.
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
        plugins_dir: Optional[str] = None,
    ):
        """
        Initialize the Frame instance.

        This constructor sets up the Frame with the necessary API keys and
        initializes the language model service. It also sets the default
        model to be used for completions and loads plugins.

        Args:
            openai_api_key (Optional[str]): API key for OpenAI services.
            mistral_api_key (Optional[str]): API key for Mistral services.
            huggingface_api_key (Optional[str]): API key for Hugging Face services.
            default_model (Optional[str]): The default language model to use.
            plugins_dir (Optional[str]): The directory containing plugins.
        """
        self._default_model = default_model
        # Initialize the language model service with provided API keys
        # Initialize the language model service with provided API keys
        self.llm_service = LLMService(
            openai_api_key=openai_api_key,
            mistral_api_key=mistral_api_key,
            huggingface_api_key=huggingface_api_key,
            default_model=self._default_model,
        )
        self.plugins_dir = plugins_dir or os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "plugins"
        )
        self.plugins = {}
        self.is_loading_plugins = True
        self.plugins, conflict_warnings = load_plugins(self.plugins_dir)
        for warning in conflict_warnings:
            logger.warning(warning)
        logger.info(f"Loaded plugins: {list(self.plugins.keys())}")
        self.framer_factory = FramerFactory(
            FramerConfig(name="DefaultFramer", default_model=self._default_model),
            self.llm_service,
            plugins=self.plugins,
        )
        self.is_loading_plugins = False

    def set_plugins_dir(self, plugins_dir: str):
        """
        Set a custom directory for loading plugins.

        Args:
            plugins_dir (str): The directory path where plugins are located.
        """
        self.plugins_dir = plugins_dir
        self.plugins = load_plugins(self.plugins_dir)

    def create_framer(self, config: FramerConfig, **kwargs: Any) -> Framer:
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
        return self.framer_factory.create_framer(config, **kwargs)

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

    def get_metrics(self) -> Dict[str, Any]:
        """
        Get the current LLM usage metrics.

        Returns:
            A dictionary containing the call count and cost for each model,
            as well as the total calls and total cost.
        """
        return self.llm_service.get_metrics()

    def shut_down(self, save_state: bool = False, reset: bool = True):
        """
        Shut down the Frame instance, managing all Framers and workflows.

        This method handles the graceful shutdown of all Framers and their associated
        workflows. It can optionally save the current state and reset the Frame.

        Args:
            save_state (bool): If True, save the current state of all Framers and workflows.
                               Defaults to False.
            reset (bool): If True, reset all Framers and workflows after shutdown.
                          Defaults to True.

        Returns:
            None
        """
        # Implement logic to pause or stop all workflows
        # if hasattr(self, 'framers'):
        #     for framer in self.framers:
        #         if hasattr(framer, 'workflow_manager'):
        #             framer.workflow_manager.pause_all_workflows()

        # Implement logic to save state if requested
        if save_state:
            # Save state of all Framers and workflows
            pass

        # Implement logic to remove all Framers
        # if hasattr(self, 'framers'):
        #     self.framers.clear()

        # Implement logic to reset everything if requested
        if reset:
            # Reset all Frame components
            pass

        # Implement any necessary cleanup for plugins
        for plugin in self.plugins.values():
            if hasattr(plugin, "on_shutdown"):
                plugin.on_shutdown()

        # Implement any final cleanup or resource release
        # if hasattr(self, 'llm_service') and hasattr(self.llm_service, 'close'):
        #     self.llm_service.close()

        logger.info("Frame has been shut down.")


import os
import importlib
from typing import Dict, Any, Tuple, List
from dotenv import load_dotenv
from frame.src.utils.plugin_loader import load_plugin_config
from frame.src.framer.brain.plugins.base import BasePlugin
import logging

logger = logging.getLogger(__name__)


def load_plugins(plugins_dir: str) -> Tuple[Dict[str, Any], List[str]]:
    """
    Load all plugins from the specified directory.

    This function scans the given directory for plugin modules, loads them,
    and returns a dictionary of plugin names and their corresponding classes.
    It also checks for conflicting action names across plugins and handles them.

    Args:
        plugins_dir (str): The directory containing the plugins.

    Returns:
        Tuple[Dict[str, Any], List[str]]: A tuple containing:
            - A dictionary of loaded plugins, where the key is the plugin name
              and the value is the plugin class.
            - A list of warning messages for conflicting actions.
    """
    # Load environment variables from .env file
    load_dotenv()

    plugins = {}
    loaded_actions = {}
    conflict_warnings = []

    for item in os.listdir(plugins_dir):
        plugin_dir = os.path.join(plugins_dir, item)
        if os.path.isdir(plugin_dir) and not item.startswith("_"):
            try:
                # Load plugin-specific configuration
                config = load_plugin_config(plugin_dir)

                # Import the plugin module
                logger.debug(f"Attempting to import module for plugin: {item}")
                module = importlib.import_module(f"plugins.{item}.{item}")
                logger.debug(f"Module imported successfully for plugin: {item}")

                # Construct the plugin class name by converting the directory name to CamelCase
                plugin_class_name = "".join(
                    word.capitalize() for word in item.split("_")
                )
                logger.debug(f"Looking for class {plugin_class_name} in module {item}")
                plugin_class = getattr(module, plugin_class_name, None)
                if plugin_class is None:
                    logger.warning(
                        f"Class {plugin_class_name} not found in module {item}. Skipping."
                    )
                    continue

                # Check if the plugin class inherits from PluginBase
                if not issubclass(plugin_class, BasePlugin):
                    logger.warning(
                        f"Plugin {item} does not inherit from PluginBase. Skipping."
                    )
                    continue

                # Initialize the plugin with its configuration
                logger.debug(f"Initializing plugin {item} with configuration")
                plugin_instance = plugin_class(config)

                # Check for conflicting actions
                plugin_actions = plugin_instance.get_actions()
                for action_name, action_func in plugin_actions.items():
                    if action_name in loaded_actions:
                        conflict_warnings.append(
                            f"Action '{action_name}' in plugin '{item}' conflicts with an existing action. Skipping."
                        )
                    else:
                        loaded_actions[action_name] = action_func

                # Add the plugin to the plugins dictionary
                plugins[item] = plugin_instance
                logger.info(f"Loaded plugin: {item}")
            except (ImportError, AttributeError) as e:
                logger.error(f"Failed to load plugin {item}: {str(e)}", exc_info=True)

    for warning in conflict_warnings:
        logger.warning(warning)
    return plugins, conflict_warnings
