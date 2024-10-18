from typing import Optional, Dict, Any, List

from frame.src.framed.config import FramedConfig
from frame.src.framed.framed import Framed
from frame.src.framer.agency import Agency
from frame.src.framer.brain import Brain
from frame.src.framer.soul import Soul
from frame.src.framer.agency.workflow import WorkflowManager
from frame.src.services import MemoryService
from frame.src.services import EQService
from frame.src.services import ExecutionContext
from frame.src.services import LLMService

class FramedFactory:
    """
    Factory class for creating Framed instances.

    This class encapsulates the logic for constructing Framed objects,
    ensuring that all necessary components are properly initialized.
    """

    def __init__(self, config: FramedConfig, llm_service: LLMService):
        """
        Initialize the FramedFactory with configuration and LLM service.

        Args:
            config (FramedConfig): Configuration for the Framed.
            llm_service (LLMService): Language model service for text generation.
        """
        if not isinstance(config, FramedConfig):
            raise TypeError("config must be an instance of FramedConfig")
        if not isinstance(llm_service, LLMService):
            llm_service = LLMService()  # Ensure llm_service is instantiated
        self.config = config
        self.llm_service = llm_service
        self.plugins: Dict[str, Any] = {}

    async def create_framed(
        self,
        soul_seed: Optional[str] = None,
        memory_service: Optional[MemoryService] = None,
        eq_service: Optional[EQService] = None,
        roles: Optional[List[Dict[str, Any]]] = None,
        goals: Optional[List[Dict[str, Any]]] = None,
    ) -> Framed:
        return await FramedFactory(self.config, self.llm_service).create_framed(
            soul_seed=soul_seed,
            memory_service=memory_service,
            eq_service=eq_service,
            roles=roles,
            goals=goals,
        )

    async def create_framed(
        self,
        soul_seed: Optional[str] = None,
        memory_service: Optional[MemoryService] = None,
        eq_service: Optional[EQService] = None,
        roles: Optional[List[Dict[str, Any]]] = None,
        goals: Optional[List[Dict[str, Any]]] = None,
    ) -> Framed:
        builder = FramedBuilder(self.config, self.llm_service)
        builder.with_soul_seed(soul_seed)
        builder.with_memory_service(memory_service)
        builder.with_eq_service(eq_service)
        builder.with_roles(roles)
        builder.with_goals(goals)
        framed = await builder.build()
        await framed.initialize()
        return framed

    def get_plugin(self, plugin_name: str) -> Any:
        """
        Retrieve a plugin by name.

        Args:
            plugin_name (str): The name of the plugin to retrieve.

        Returns:
            Any: The plugin object if found, otherwise None.
        """
        return self.plugins.get(plugin_name)


class FramedBuilder:
    """
    Builder class for constructing Framed instances.

    This class provides a flexible interface for configuring and
    creating Framed objects using the FramedFactory.
    """

    def __init__(self, config: FramedConfig, llm_service: LLMService):
        if not isinstance(config, FramedConfig):
            raise ValueError("Config must be an instance of FramedConfig")
        self.config = config
        if not isinstance(llm_service, LLMService):
            raise ValueError("llm_service must be an instance of LLMService")
        self.llm_service = llm_service
        self.soul_seed = None
        self.memory_service = None
        self.eq_service = None
        self.roles = None
        self.goals = None

    def with_soul_seed(self, soul_seed: Optional[str]) -> "FramedBuilder":
        self.soul_seed = soul_seed
        return self

    def with_memory_service(
        self, memory_service: Optional[MemoryService]
    ) -> "FramedBuilder":
        self.memory_service = memory_service
        return self

    def with_eq_service(self, eq_service: Optional[EQService]) -> "FramedBuilder":
        self.eq_service = eq_service
        return self

    def with_roles(self, roles: Optional[List[Dict[str, Any]]]) -> "FramedBuilder":
        self.roles = roles
        return self

    def with_goals(self, goals: Optional[List[Dict[str, Any]]]) -> "FramedBuilder":
        self.goals = goals
        return self

    async def build(self) -> Framed:
        execution_context = ExecutionContext(llm_service=self.llm_service)
        agency = Agency(
            llm_service=self.llm_service,
            execution_context=execution_context,
            context=None,
        )
        brain = Brain(
            llm_service=self.llm_service,
            default_model=self.config.default_model,
            roles=self.roles or [],
            goals=self.goals or [],
        )

        soul_seed = self.soul_seed or {"seed": f"Default seed for {self.config.name}"}
        soul = Soul(seed=soul_seed)
        workflow_manager = WorkflowManager()

        framed = Framed(
            config=self.config,
            llm_service=self.llm_service,
            agency=agency,
            brain=brain,
            soul=soul,
            workflow_manager=workflow_manager,
            memory_service=self.memory_service,
            eq_service=self.eq_service,
            roles=self.roles,
            goals=self.goals,
        )

        await framed.initialize()
        return framed
