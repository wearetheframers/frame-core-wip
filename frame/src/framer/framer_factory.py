from typing import Optional, Dict, Any, Union, List
from frame.src.framer.framer import Framer

# Import necessary components for Framer creation
from frame.src.framer.config import FramerConfig
from frame.src.services.llm.main import LLMService
from frame.src.framer.agency.agency import Agency
from frame.src.framer.brain.brain import Brain
from frame.src.framer.soul.soul import Soul
from frame.src.framer.agency.workflow import WorkflowManager
from frame.src.services.context.execution_context_service import ExecutionContext
from frame.src.services.memory.main import MemoryService
from frame.src.services.eq.main import EQService
from frame.src.constants.models import DEFAULT_MODEL
import logging
from frame.src.framer.agency.goals import Goal, GoalStatus
from frame.src.framer.agency.roles import Role, RoleStatus
from frame.src.framer.brain.memory.memory_adapters.mem0_adapter import Mem0Adapter


class FramerFactory:
    """
    Factory class for creating Framer instances.

    This class encapsulates the logic for constructing Framer objects,
    ensuring that all necessary components are properly initialized.

    The Framer includes a `halt()` method to stop its actions and task processing.

    The FramerFactory supports the creation of Framers with custom plugins,
    allowing for extensive customization and expansion of capabilities.
    This plugin system is designed to be as flexible and powerful as mods in games,
    enabling developers to create a wide range of extensions and enhancements.
    """

    def __init__(
        self,
        config: FramerConfig,
        llm_service: LLMService,
        plugins: Optional[Dict[str, Any]] = [],
    ):
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
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.llm_service = llm_service
        self.plugins = plugins

    async def create_framer(
        self,
        memory_service: Optional[MemoryService] = None,
        eq_service: Optional[EQService] = None,
        roles: Optional[List[Role]] = None,
        goals: Optional[List[Goal]] = None,
        plugins: Optional[Dict[str, Any]] = None,
    ) -> Framer:
        self.plugins = plugins or {}
        execution_context = ExecutionContext(llm_service=self.llm_service)
        agency = Agency(
            llm_service=self.llm_service,
            execution_context=execution_context,
            context=None,
        )
        # Initialize the Agency component with default permissions
        self.config.permissions = self.config.permissions or [
            "with_memory",
            "with_mem0_search_extract_summarize_plugin",
            "with_shared_context",
        ]
        roles, goals = await self._generate_roles_and_goals(agency, roles, goals)
        brain = Brain(
            # Initialize the Brain component with roles, goals, and default model
            llm_service=self.llm_service,
            roles=roles,
            goals=goals,
            default_model=(
                self.config.default_model
                if self.config.default_model
                else DEFAULT_MODEL
            ),
        )
        # Initialize the Soul component with the provided or default seed
        soul = Soul(seed=self.config.soul_seed)
        # Initialize the WorkflowManager component
        workflow_manager = WorkflowManager()
        # Set the memory service if provided, otherwise create a new one
        memory_service = memory_service or MemoryService(adapter=Mem0Adapter())

        framer = Framer(
            config=self.config,
            llm_service=self.llm_service,
            agency=agency,
            brain=brain,
            soul=soul,
            workflow_manager=workflow_manager,
            memory_service=memory_service,
            eq_service=eq_service,
            plugins=plugins,
        )

        framer.agency.set_goals(goals)
        framer.agency.set_roles(roles)

        # Set the Framer instance in Brain and ActionRegistry
        framer.brain.set_framer(framer)
        framer.brain.agency.action_registry.set_framer(framer)

        # Notify observers about the Framer being opened
        for observer in framer.observers:
            if hasattr(observer, "on_framer_opened"):
                observer.on_framer_opened(framer)

        # Call on_load for each plugin
        for plugin_name, plugin_instance in framer.plugins.items():
            if hasattr(plugin_instance, "on_load"):
                self.logger.info(f"Loading plugin: {plugin_name}")
                await plugin_instance.on_load(framer)
                self.logger.info(f"Plugin {plugin_name} loaded successfully.")

        framer.plugin_loading_complete = True

        return framer

    async def _generate_roles_and_goals(self, agency, roles, goals):
        if roles is None or goals is None:
            roles, goals = await agency.generate_roles_and_goals()
        elif isinstance(roles, list) and len(roles) == 0:
            roles = []
            goals = []
        elif isinstance(goals, list) and len(goals) == 0:
            roles, goals = await agency.generate_roles_and_goals()
            goals = []
        elif isinstance(roles, list) and len(roles) == 0 and goals:
            roles, new_goals = await agency.generate_roles_and_goals()
            goals.extend(new_goals)

        # Ensure goals have a default status of ACTIVE
        for goal in goals:
            if isinstance(goal, dict):
                if "status" not in goal:
                    goal["status"] = GoalStatus.ACTIVE.value
            else:
                goal.status = GoalStatus.ACTIVE
        for role in roles:
            if isinstance(role, dict):
                if "status" not in role:
                    role["status"] = RoleStatus.ACTIVE.value
            else:
                role.status = RoleStatus.ACTIVE

        # Sort roles and goals by priority
        roles.sort(
            key=lambda x: x.priority.value if hasattr(x, "priority") else 5,
            reverse=True,
        )
        goals.sort(
            key=lambda x: x.priority.value if hasattr(x, "priority") else 5,
            reverse=True,
        )

        return roles, goals


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
        return await FramerFactory(self.config, self.llm_service).create_framer()
