import os
from typing import Optional, Dict, Any, Union, List
from frame.src.framer.framer import Framer

# Import necessary components for Framer creation
from frame.src.framer.config import FramerConfig
from frame.src.services import LLMService
from frame.src.framer.agency import Agency, Goal, GoalStatus, Role, RoleStatus
from frame.src.framer.brain import Brain, Mind
from frame.src.models.framer.soul.soul import Soul
from frame.src.framer.agency import WorkflowManager
from frame.src.services import ExecutionContext, EQService, MemoryService
from frame.src.constants import DEFAULT_MODEL
from frame.src.framer.brain.memory.memory_adapters import Mem0Adapter

import logging


class FramerFactory:
    """
    Factory class for creating Framer instances.

    This class encapsulates the logic for constructing Framer objects,
    ensuring that all necessary components are properly initialized and configured.

    Key features:
    - Creates fully initialized Framer instances with all required components
    - Supports custom plugin integration for extended functionality
    - Ensures proper initialization of core services like LLM, memory, and EQ
    - Manages role and goal generation for the Framer
    - Handles the loading and configuration of plugins

    The FramerFactory supports the creation of Framers with custom plugins,
    allowing for extensive customization and expansion of capabilities.
    This plugin system is designed to be as flexible and powerful as mods in games,
    enabling developers to create a wide range of extensions and enhancements.

    Note: The Framer includes a `halt()` method to stop its actions and task processing,
    which can be used for graceful shutdown or pausing of the Framer's operations.
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
        from unittest.mock import MagicMock

        if not isinstance(config, FramerConfig) and not isinstance(config, MagicMock):
            raise TypeError(
                "config must be an instance of FramerConfig or a MagicMock for testing"
            )
        if not isinstance(llm_service, LLMService):
            raise TypeError("llm_service must be an instance of LLMService")
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.llm_service = llm_service
        self.plugins = plugins
        self.permissions = config.permissions or []

    async def create_framer(
        self,
        memory_service: Optional[MemoryService] = None,
        eq_service: Optional[EQService] = None,
        roles: Optional[List[Role]] = None,
        goals: Optional[List[Goal]] = None,
        plugins: Optional[Dict[str, Any]] = None,
    ) -> Framer:
        self.plugins = plugins or {}
        execution_context = ExecutionContext(
            llm_service=self.llm_service,
            soul=None,  # We'll set this later
            brain=None,  # We'll set this later
            config=self.config,
        )
        agency = Agency(
            llm_service=self.llm_service,
            execution_context=execution_context,
            context=None,
        )
        # Initialize the Agency component without default permissions
        # Users must add all permissions for any plugins they want to use
        self.config.permissions = self.config.permissions or []
        roles, goals = await self._generate_unique_roles_and_goals(agency, roles, goals)

        # Initialize the Soul component with the provided or default seed
        soul = Soul(
            seed=(
                self.config.soul_seed
                if isinstance(self.config.soul_seed, (str, dict, type(None)))
                else None
            )
        )
        # Initialize the WorkflowManager component
        workflow_manager = WorkflowManager()
        # Set the memory service if provided, otherwise create a new one if with_memory permission is present
        if "with_memory" in self.config.permissions:
            mem0_adapter = Mem0Adapter(api_key=self.config.mem0_api_key)
            memory_service = memory_service or MemoryService(adapter=mem0_adapter)
        # Initialize the Brain component with roles, goals, default model
        brain = Brain(
            llm_service=self.llm_service,
            execution_context=execution_context,
            memory_service=memory_service,
            roles=roles,
            goals=goals,
            default_model=(
                self.config.default_model
                if self.config.default_model
                else DEFAULT_MODEL
            ),
            soul=soul,
        )

        # The Mind is now initialized within the Brain constructor
        mind = brain.mind
        execution_context = ExecutionContext(llm_service=self.llm_service)
        execution_context.agency = agency
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
            execution_context=execution_context,
        )

        framer.agency.set_goals(goals)
        framer.agency.set_roles(roles)

        # Set the Framer instance in Brain
        framer.brain.set_framer(framer)

        # Notify observers about the Framer being opened
        for observer in framer.observers:
            if hasattr(observer, "on_framer_opened"):
                observer.on_framer_opened(framer)

        # Load plugins only if they are default or included in permissions
        for plugin_name, plugin_instance in (plugins or {}).items():
            permission_name = f"with_{plugin_name}"
            if (
                plugin_name in os.getenv("DEFAULT_PLUGINS", "").split(",")
                or permission_name in self.config.permissions
            ):
                self.plugins[plugin_name] = plugin_instance
                if hasattr(plugin_instance, "on_load"):
                    self.logger.info(f"Loading plugin: {plugin_name}")
                    await plugin_instance.on_load(framer)
                    self.logger.info(f"Plugin {plugin_name} loaded successfully.")
            else:
                self.logger.info(
                    f"Plugin {plugin_name} not loaded due to missing permission or not being a default plugin."
                )

        framer.plugin_loading_complete = True

        return framer

    async def _generate_unique_roles_and_goals(self, agency, roles, goals):
        if roles is None or goals is None:
            roles, goals = await agency.generate_roles_and_goals()
        elif isinstance(roles, list) and len(roles) == 0:
            roles, _ = await agency.generate_roles_and_goals()
        elif isinstance(goals, list) and len(goals) == 0:
            _, goals = await agency.generate_roles_and_goals()

        # Ensure uniqueness of roles and goals
        unique_roles = {role.name: role for role in roles}
        unique_goals = {goal.name: goal for goal in goals}

        # Ensure goals and roles have a default status of ACTIVE
        for item in list(unique_roles.values()) + list(unique_goals.values()):
            if isinstance(item, dict):
                item["status"] = item.get("status", GoalStatus.ACTIVE.value)
            else:
                item.status = getattr(item, "status", GoalStatus.ACTIVE)
        priority = lambda x: (
            x.priority
            if isinstance(x.priority, int)
            else x.priority.value if hasattr(x, "priority") else 5
        )
        # Sort roles and goals by priority
        sorted_roles = sorted(
            unique_roles.values(),
            key=priority,
            reverse=True,
        )
        sorted_roles = sorted(
            unique_roles.values(),
            key=priority,
            reverse=True,
        )
        sorted_goals = sorted(
            unique_goals.values(),
            key=priority,
            reverse=True,
        )

        return sorted_roles, sorted_goals


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
