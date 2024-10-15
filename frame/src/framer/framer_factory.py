from typing import Optional, Dict, Any
from frame.src.framer.framer import Framer

# Import necessary components for Framer creation
from frame.src.framer.config import FramerConfig
from frame.src.services.llm.main import LLMService
from frame.src.framer.agency.agency import Agency
from frame.src.framer.brain.brain import Brain
from frame.src.framer.soul.soul import Soul
from frame.src.framer.agency.tasks.workflow.workflow_manager import WorkflowManager
from frame.src.services.memory.main import MemoryService
from frame.src.services.eq.main import EQService


class FramerFactory:
    """
    Factory class for creating Framer instances.

    This class encapsulates the logic for constructing Framer objects,
    ensuring that all necessary components are properly initialized.
    """

    def __init__(self, config: FramerConfig, llm_service: LLMService):
        """
        Initialize the FramerBuilder with configuration and LLM service.

        Args:
            config (FramerConfig): Configuration for the Framer.
            llm_service (LLMService): Language model service for text generation.
        """
        """
        Initialize the FramerFactory with configuration and LLM service.

        Args:
            config (FramerConfig): Configuration for the Framer.
            llm_service (LLMService): Language model service for text generation.
        """
        if not isinstance(config, FramerConfig):
            raise TypeError("config must be an instance of FramerConfig")
        if not isinstance(llm_service, LLMService):
            raise TypeError("llm_service must be an instance of LLMService")
        self.config = config
        self.llm_service = llm_service
        self.plugins: Dict[str, Any] = {}

    async def create_framer(
        self,
        soul_seed: Optional[Dict[str, str]] = None,
        memory_service: Optional[MemoryService] = None,
        eq_service: Optional[EQService] = None,
    ) -> Framer:
        agency = Agency(llm_service=self.llm_service, context=None)
        # Initialize the Agency component with the LLM service
        brain = Brain(
            # Initialize the Brain component with default model, roles, and goals
            llm_service=self.llm_service,
            default_model=self.config.default_model,
            roles=[],
            goals=[],
        )

        if soul_seed is None:
            # Generate a default soul seed if none is provided
            soul_seed = f"Default seed for {self.config.name}"

        soul = Soul(
            seed=(
                {"seed": soul_seed.get("seed")}
                if isinstance(soul_seed, dict)
                else {"seed": soul_seed}
            )
        )
        # Initialize the Soul component with the provided or default seed
        workflow_manager = WorkflowManager()
        # Initialize the WorkflowManager component

        from frame.src.framer.framer import Framer  # Import Framer within the function

        framer = Framer(
            # Create the Framer instance with all initialized components
            config=self.config,
            llm_service=self.llm_service,
            agency=agency,
            brain=brain,
            soul=soul,
            workflow_manager=workflow_manager,
            memory_service=memory_service,
            eq_service=eq_service,
        )

        return framer

    def get_plugin(self, plugin_name: str) -> Any:
        """
        Retrieve a plugin by name.

        Args:
            plugin_name (str): The name of the plugin to retrieve.

        Returns:
            Any: The plugin object if found, otherwise None.
        """
        return self.plugins.get(plugin_name)


class FramerBuilder:
    """
    Builder class for constructing Framer instances.

    This class provides a flexible interface for configuring and
    creating Framer objects using the FramerFactory.
    """

    def __init__(self, config: FramerConfig, llm_service: LLMService):
        if not isinstance(config, FramerConfig):
            raise ValueError("Config must be an instance of FramerConfig")
        self.config = config
        if not isinstance(llm_service, LLMService):
            raise ValueError("llm_service must be an instance of LLMService")
        self.llm_service = llm_service

    async def build(self) -> Framer:
        """
        Asynchronously build a Framer instance.

        Returns:
            Framer: A new Framer instance, fully configured and ready to use.
        """
        factory = FramerFactory(self.config, self.llm_service)
        return await factory.create_framer()
