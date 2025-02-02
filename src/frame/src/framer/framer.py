import asyncio
import logging
import time
import json
import concurrent.futures
from frame.src.utils.decorators import (
    log_execution,
    validate_input,
    measure_performance,
)
from collections import deque
from typing import List, Dict, Any, Optional, Callable, Union, Tuple, Deque

from frame.src.framer.config import FramerConfig
from frame.src.framer.agency import Agency, Role, RoleStatus
from frame.src.framer.agency.workflow import WorkflowManager
from frame.src.framer.agency.tasks import Task, TaskStatus
from frame.src.framer.agency.goals import Goal, GoalStatus
from frame.src.framer.brain import Brain
from frame.src.framer.brain.decision import Decision
from frame.src.models.framer.soul import Soul
from frame.src.framer.brain.mind.perception import Perception
from frame.src.models.framer.soul import Soul

from frame.src.services.context.execution_context_service import ExecutionContext
from frame.src.services.eq import EQService
from frame.src.services.llm import LLMService
from frame.src.services.memory import MemoryService
from frame.src.services.context.shared_context_service import SharedContext

from frame.src.utils.config_parser import (
    execution_context_to_json,
    execution_context_from_json,
    parse_json_config,
    parse_markdown_config,
    export_config_to_markdown,
)

from frame.src.framer.brain.memory.memory_adapters import Mem0Adapter
from frame.src.framer.brain.memory.memory_adapter_interface import (
    MemoryAdapterInterface,
)

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from frame.src.framer.brain import Brain

Observer = Callable[[Decision], None]

logger = logging.getLogger("frame.framer")


class Framer:
    @classmethod
    async def create(cls, config: FramerConfig, llm_service: LLMService):
        from frame.src.framer.framer_factory import FramerFactory

        factory = FramerFactory(config, llm_service)
        framer = await factory.create_framer(
            memory_service=None,
            eq_service=None,
        )
        await framer._generate_initial_roles_and_goals()
        return framer

    perceptions_queue: Deque[Union[Perception, Dict[str, Any]]] = deque()
    """
    The Framer class represents an AI agent with advanced cognitive capabilities. It integrates various components
    such as agency, brain, soul, and workflow management to create a comprehensive AI entity capable of
    processing perceptions, making decisions, and executing tasks in a context-aware manner.

    Key features:
    - Perception processing and decision-making
    - Task execution and workflow management
    - Memory management and retrieval
    - Emotional intelligence integration
    - Plugin system for extensibility
    - Role and goal management
    - Observer pattern for decision notifications

    Attributes:
        config (FramerConfig): Configuration settings for the Framer.
        llm_service (LLMService): The language model service used by the Framer for text generation and processing.
        agency (Agency): Manages roles, goals, tasks, and workflows for the Framer.
        brain (Brain): Handles decision-making processes, integrating perceptions, memories, and thoughts.
        soul (Soul): Represents the core essence and personality of the Framer.
        workflow_manager (WorkflowManager): Manages workflows and tasks.
        memory_service (Optional[MemoryService]): Service for managing and retrieving memories. Default is None.
        eq_service (Optional[EQService]): Service for managing emotional intelligence. Default is None.
        roles (Optional[List[Dict[str, Any]]]): List of roles for the Framer. Default is None.
        goals (Optional[List[Dict[str, Any]]]): List of goals for the Framer. Default is None.
        observers (List[Observer]): List of observer functions to notify on decisions.
        can_execute (bool): Determines if decisions are executed automatically. Default is True.
        acting (bool): Indicates if the Framer is actively processing perceptions. Default is False.
        plugins (Dict[str, Any]): Dictionary of loaded plugins for extended functionality.
        plugin_loading_complete (bool): Indicates whether all plugins have been loaded.
        permissions (List[str]): List of permissions granted to the Framer.

    The Framer class serves as the central coordinator for all AI agent operations, managing the interplay
    between various components to create a cohesive and intelligent entity.
    """

    def __init__(
        self,
        config: FramerConfig,
        llm_service: LLMService,
        agency: Agency,
        soul: Soul,
        workflow_manager: WorkflowManager,
        brain: Optional[Brain] = None,
        memory_adapter: Optional[MemoryAdapterInterface] = None,
        memory_service: Optional[MemoryService] = None,
        eq_service: Optional[EQService] = None,
        roles: List[Dict[str, Any]] = [],
        goals: List[Dict[str, Any]] = [],
        plugins: Optional[Dict[str, Any]] = None,
        plugin_loading_progress: Optional[Callable[[int], None]] = None,
        execution_context: Optional[ExecutionContext] = None,
    ):
        self.llm_service = llm_service
        self.memory_service = memory_service
        self.eq_service = eq_service
        self.plugin_loading_progress = plugin_loading_progress
        self.config = config
        self.permissions = config.permissions or []
        self.llm_service = llm_service

        self.execution_context = execution_context or ExecutionContext(
            llm_service=self.llm_service, soul=soul, config=config
        )
        self.execution_context.soul = soul
        self.execution_context.brain = brain
        self.execution_context.set_roles(roles)
        self.execution_context.set_goals(goals)

        # Initialize services and plugins based on permissions

        if "with_memory" in self.permissions:
            self.memory_service = memory_service or MemoryService(
                adapter=memory_adapter or Mem0Adapter(api_key=self.config.mem0_api_key)
            )
        else:
            self.memory_service = None

        if "with_eq" in self.permissions:
            self.eq_service = eq_service or EQService()

        if "with_shared_context" in self.permissions:
            self.shared_context_service = SharedContext(llm_service=self.llm_service)

        self.agency = agency
        self.soul = soul
        self.workflow_manager = workflow_manager
        self.roles = roles or []
        self.goals = goals or []
        self.plugins = {}
        self.plugin_loading_complete = False
        self.plugin_loading_complete = False
        self._streamed_response = {"status": "pending", "result": ""}
        self._streaming_task = None

        logger.info("Creating Brain")
        self.brain = Brain(
            llm_service=llm_service,
            execution_context=self.execution_context,
            memory_service=self.memory_service,
            roles=self.roles,
            goals=self.goals,
            default_model=config.default_model,
            soul=soul,
        )
        logger.info(f"Brain created with memory service: {self.brain.memory_service}")
        self.brain.action_registry.set_execution_context(self.execution_context)

        self._dynamic_model_choice = False
        self.observers: List[Observer] = []
        self.can_execute = True
        self.acting = True

    async def initialize(self):
        """
        Initialize the Framer by generating initial roles and goals if not provided.
        """
        if not self.roles or not self.goals:
            self.roles, self.goals = await self.agency.generate_roles_and_goals()

        # Ensure uniqueness
        if not self.roles:
            self.roles = list(
                {
                    (
                        role.name
                        if isinstance(role, Role)
                        else getattr(role, "get", lambda k, d=None: d)(
                            "name", "default_name"
                        )
                    ): (
                        role
                        if isinstance(role, Role)
                        else {
                            "id": "default_id",
                            "name": role,
                            "description": "default_description",
                            "permissions": [],
                            "priority": 5,
                            "status": RoleStatus.ACTIVE,
                        }
                    )
                    for role in self.roles
                }.values()
            )
        self.goals = list(
            {
                (
                    goal.description
                    if isinstance(goal, Goal)
                    else (
                        goal
                        if isinstance(goal, str)
                        else goal.get("description", "default_description")
                    )
                ): (
                    goal
                    if isinstance(goal, Goal)
                    else Goal(
                        name=(
                            "default_name"
                            if isinstance(goal, str)
                            else goal.get("name", "default_name")
                        ),
                        description=(
                            goal
                            if isinstance(goal, str)
                            else goal.get("description", "default_description")
                        ),
                    )
                )
                for goal in self.goals
            }.values()
        )

        logger.info(
            f"Generated initial roles: {[role.name if isinstance(role, Role) else role['name'] for role in self.roles]}"
        )
        logger.info(
            f"Generated initial goals: {[goal['description'] if isinstance(goal, dict) else goal.description for goal in self.goals]}"
        )

        if hasattr(self.brain, "set_roles"):
            self.brain.set_roles(self.roles)
        if hasattr(self.brain, "set_goals"):
            self.brain.set_goals(self.goals)

        if hasattr(self.execution_context, "set_roles"):
            self.execution_context.set_roles(self.roles)
        if hasattr(self.execution_context, "set_goals"):
            self.execution_context.set_goals(self.goals)
        await self.load_plugins()

    async def load_plugins(self):
        """
        Load all plugins by calling their on_load method.
        """
        logger.info(f"Loading plugins for Framer with config: {self.config}")
        loaded_plugins = set()

        def load_plugin(plugin_name, plugin_instance):
            if (
                plugin_name in loaded_plugins
                or any(
                    isinstance(existing_plugin, type(plugin_instance))
                    for existing_plugin in loaded_plugins
                )
                or plugin_instance in loaded_plugins
            ):
                logger.info(f"Plugin {plugin_name} already loaded. Skipping.")
                return

            if hasattr(plugin_instance, "on_load"):
                asyncio.run(plugin_instance.on_load(self))
                # Register plugin actions in the brain's action_registry
                for action_name, action_func in plugin_instance.get_actions().items():
                    if action_name not in self.brain.action_registry.actions:
                        self.brain.action_registry.add_action(
                            action_name,
                            action_func=action_func,
                            description=f"Action from {plugin_name} plugin",
                            priority=5,  # Default priority, adjust as needed
                        )
                    else:
                        logger.info(
                            f"Action {action_name} already registered. Skipping."
                        )
                loaded_plugins.add(plugin_name)
                loaded_plugins.add(plugin_instance)

        if "all" in self.plugins:
            for plugin_name, plugin_instance in self.plugins.items():
                load_plugin(plugin_name, plugin_instance)
        else:
            with concurrent.futures.ProcessPoolExecutor() as executor:
                futures = [
                    executor.submit(load_plugin, plugin_name, plugin_instance)
                    for plugin_name, plugin_instance in self.plugins.items()
                ]
                for future in concurrent.futures.as_completed(futures):
                    future.result()

        with concurrent.futures.ProcessPoolExecutor() as executor:
            futures = [
                executor.submit(load_plugin, plugin_name, plugin_instance)
                for plugin_name, plugin_instance in self.plugins.items()
            ]
            for future in concurrent.futures.as_completed(futures):
                future.result()
        self.plugin_loading_complete = True
        self.act()
        await self.process_queued_perceptions()

        # Generate roles and goals if not provided
        if not self.roles or not self.goals:
            asyncio.create_task(self._generate_initial_roles_and_goals())

    @log_execution
    @measure_performance
    async def _generate_initial_roles_and_goals(self):
        if not self.roles or not self.goals:
            self.roles, self.goals = await self.agency.generate_roles_and_goals()

        # Ensure uniqueness
        self.roles = list(
            {
                role["name"] if isinstance(role, dict) else role.name: role
                for role in self.roles
            }.values()
        )
        self.goals = list(
            {
                (
                    goal["description"] if isinstance(goal, dict) else goal.description
                ): goal
                for goal in self.goals
            }.values()
        )

        logger.info(
            f"Generated initial roles: {[role['name'] if isinstance(role, dict) else role.name for role in self.roles]}"
        )
        logger.info(
            f"Generated initial goals: {[goal['description'] if isinstance(goal, dict) else goal.description for goal in self.goals]}"
        )

        if hasattr(self.brain, "set_roles"):
            self.brain.set_roles(self.roles)
        if hasattr(self.brain, "set_goals"):
            self.brain.set_goals(self.goals)

        if hasattr(self.execution_context, "set_roles"):
            self.execution_context.set_roles(self.roles)
        if hasattr(self.execution_context, "set_goals"):
            self.execution_context.set_goals(self.goals)

    def act(self):
        """
        Enable the Framer to start acting and processing perceptions.
        """
        self.acting = True

    def add_plugin(self, plugin_name: str, plugin_instance: Any):
        """
        Add a plugin to the Framer.

        Args:
            plugin_name (str): The name of the plugin.
            plugin_instance (Any): The plugin instance to add.
        """
        self.plugins[plugin_name] = plugin_instance
        if hasattr(plugin_instance, "on_load"):
            asyncio.create_task(plugin_instance.on_load(self))

    async def add_plugins(self, plugins: Dict[str, Any]):
        """
        Add multiple plugins to the Framer.

        Args:
            plugins (Dict[str, Any]): A dictionary of plugin names and instances to add.
        """
        for plugin_name, plugin_instance in plugins.items():
            self.add_plugin(plugin_name, plugin_instance)

    async def remove_plugins(self, plugin_names: List[str]):
        """
        Remove multiple plugins from the Framer.

        Args:
            plugin_names (List[str]): A list of plugin names to remove.
        """
        for plugin_name in plugin_names:
            await self.remove_plugin(plugin_name)

    async def process_queued_perceptions(self):
        """
        Process all queued perceptions once the Framer is ready.
        """
        if self.is_ready():
            if self.perceptions_queue:
                logger.info("Processing queued perceptions before Framer was acting..")
            while self.perceptions_queue:
                logger.info(
                    f"Processing perception from queue: {self.perceptions_queue[0]}"
                )
                perception = self.perceptions_queue.popleft()
                await self.sense(perception)

            if not self.roles and not self.goals:
                self.roles, self.goals = await self.agency.generate_roles_and_goals()
            elif not self.roles:
                self.roles, _ = await self.agency.generate_roles_and_goals()
            elif not self.goals:
                _, self.goals = await self.agency.generate_roles_and_goals()

            # Sort roles and goals by priority
            self.roles.sort(
                key=lambda x: (
                    x.priority if isinstance(x, Role) else x.get("priority", 5)
                ),
                reverse=True,
            )
            self.goals.sort(
                key=lambda x: (
                    x.priority if isinstance(x, Goal) else x.get("priority", 5)
                ),
                reverse=True,
            )

            self.agency.set_roles(self.roles)
            self.agency.set_goals(self.goals)
        else:
            logger.warning("Framer is not ready. Queuing perception.")
            logger.info(f"Queued perception: {perception}")

        # Sort roles and goals by priority
        self.roles.sort(
            key=lambda x: x.priority if isinstance(x, Role) else x.get("priority", 5),
            reverse=True,
        )
        self.goals.sort(
            key=lambda x: x.priority if isinstance(x, Goal) else x.get("priority", 5),
            reverse=True,
        )

        self.agency.set_roles(self.roles)
        self.agency.set_goals(self.goals)

    async def export_to_file(self, file_path: str) -> None:
        """
        Export the Framer configuration to a JSON file.

        This method allows the Framer agent to be fully exported into a JSON format,
        making it portable and easy to use inside a prompt to any other LLM. This
        portability enables the Framer agents to be shared and consumed by other
        systems, facilitating interoperability and reuse.

        Args:
            file_path (str): The path to the file where the JSON will be saved.
        """
        config = self.config
        config.soul_seed = self.soul.seed
        config.roles = self.roles
        config.goals = self.goals
        config_dict = config.to_dict()
        config_dict["execution_context"] = execution_context_to_json(
            self.execution_context
        )
        with open(file_path, "w") as f:
            json.dump(config_dict, f, indent=4)

    @classmethod
    def load_from_file(
        cls,
        file_path: str,
        llm_service: LLMService,
        memory_service: Optional[MemoryService] = None,
        eq_service: Optional[EQService] = None,
    ) -> "Framer":
        """
        Load a Framer configuration from a file.

        This method allows importing a Framer agent from a JSON or markdown file,
        enabling the reconstruction of the agent's state and configuration. This
        functionality is crucial for restoring Framer agents from saved states,
        ensuring continuity and consistency across different sessions or environments.

        Args:
            file_path (str): The path to the configuration file.
            llm_service (LLMService): Language model service.
            memory_service (Optional[MemoryService]): Memory service for the Framer.
            eq_service (Optional[EQService]): Emotional intelligence service for the Framer.

        Returns:
            Framer: A new Framer instance configured from the file.
        """
        config = parse_json_config(file_path)
        config_data = parse_json_config(file_path)
        execution_context_data = config_data.pop("execution_context", {})
        execution_context = execution_context_from_json(
            execution_context_data, ExecutionContext
        )

        return cls(
            execution_context=execution_context,
            config=config,
            llm_service=llm_service,
            agency=Agency(llm_service=llm_service, context=None),
            brain=Brain(
                llm_service=llm_service,
                default_model=config.default_model,
                roles=config.roles if config.roles is not None else [],
                goals=config.goals if config.goals is not None else [],
                soul=Soul(seed=config.soul_seed),
            ),
            soul=Soul(seed=config.soul_seed),
            workflow_manager=WorkflowManager(),
            memory_service=memory_service,
            eq_service=eq_service,
            roles=config.roles if config.roles is not None else [],
            goals=config.goals if config.goals is not None else [],
        )

    async def export_to_markdown(self, file_path: str) -> None:
        """
        Export the Framer configuration to a Markdown file.

        This method allows the Framer agent to be fully exported into a Markdown format,
        making it portable and easy to use inside a prompt to any other LLM. This
        portability enables the Framer agents to be shared and consumed by other
        systems, facilitating interoperability and reuse.

        Args:
            file_path (str): The path to the file where the Markdown will be saved.
        """
        from frame.src.utils.config_parser import export_config_to_markdown

        export_config_to_markdown(self.config, file_path)

    async def use_plugin_action(
        self, plugin_name: str, action_name: str, parameters: Dict[str, Any]
    ) -> Any:
        """
        Execute a plugin action directly.

        Args:
            plugin_name (str): The name of the plugin.
            action_name (str): The name of the action to execute.
            parameters (Dict[str, Any]): Parameters for the action.

        Returns:
            Any: The result of the action execution.
        """
        # Get the plugin instance
        plugin = self.plugins.get(plugin_name)
        if not plugin:
            logger.warning(f"Plugin {plugin_name} not found. Skipping action.")
            return {"error": f"Plugin {plugin_name} not found."}

        action = getattr(plugin, action_name, None)
        if not action:
            raise ValueError(f"Action {action_name} not found in plugin {plugin_name}.")

        return await action(**parameters)

    async def perform_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform a task asynchronously.

        Args:
            task (Dict[str, Any]): Dictionary containing task details.

        Returns:
            Dict[str, Any]: Result of the task execution.
        """
        logger.debug(f"perform_task called with task: {task}")
        valid_task_keys = Task.__annotations__.keys()
        task_filtered = {k: v for k, v in task.items() if k in valid_task_keys}
        # Ensure required fields are present
        if "description" not in task_filtered:
            task_filtered["description"] = "Default Task Description"
        if "workflow_id" not in task_filtered:
            task_filtered["workflow_id"] = "default"

        task_obj = Task(**task_filtered)
        result = await self.perform_task(task_obj.to_dict())
        return result if result is not None else {"output": "No result returned"}

    def is_ready(self) -> bool:
        """
        Check if the Framer is ready to process perceptions and make decisions.

        Returns:
            bool: True if the Framer is ready, False otherwise.
        """
        return self.plugin_loading_complete and self.acting

    async def sense(
        self, perception: Union[Perception, Dict[str, Any]]
    ) -> Optional[Decision]:
        """
        Process a perception and make a decision.

        Args:
            perception (Union[Perception, Dict[str, Any]]): The perception to process, can be a Perception object or a dictionary.

        Returns:
            Decision: The decision made based on the perception.
        """
        if not self.is_ready():
            logger.warning("Framer is not ready. Queuing perception.")
            self.perceptions_queue.append(perception)
            return None  # Return None to indicate the perception was queued

        # Convert perception to Perception object if it is a dictionary
        if isinstance(perception, dict):
            perception = Perception.from_dict(perception)
        current_goals = self.agency.get_goals()
        decision = await self.brain.process_perception(perception, current_goals)

        if decision:
            # Handle execution based on execution_mode
            executed_decision = await self.brain.execute_decision(decision)

            # Check the status of the executed decision
            if executed_decision.status == "pending_approval":
                # Notify user or system for approval
                pass
            elif executed_decision.status == "deferred":
                # Schedule for later execution
                pass
            elif executed_decision.status == "executed":
                # Proceed as normal
                pass

            # Notify observers with the executed decision
            self.notify_observers(executed_decision)
        else:
            logger.warning("No decision was made for the given perception.")
            return None
        return decision

    async def prompt(self, text: str) -> Decision:
        """
        Process a prompt as a new perception of type 'hearing'.

        Args:
            text (str): The text of the prompt.

        Returns:
            Decision: The decision made based on the prompt.
        """
        perception_dict = {"type": "hearing", "data": {"text": text}}
        perception = Perception.from_dict(perception_dict)
        return await self.sense(perception)

    def add_observer(self, observer: Observer) -> None:
        """
        Add an observer to be notified when a decision is made.

        Args:
            observer (Observer): The observer function to add.
        """
        self.observers.append(observer)

    def remove_observer(self, observer: Observer) -> None:
        """
        Remove an observer.

        Args:
            observer (Observer): The observer function to remove.
        """
        self.observers.remove(observer)

    def notify_observers(self, decision: Decision) -> None:
        """
        Notify all observers about a decision.

        Args:
            decision (Decision): The decision to notify observers about.
        """
        for observer in self.observers:
            observer(decision)

        # Notify plugins about the decision
        for plugin in self.plugins.values():
            if hasattr(plugin, "on_decision_made"):
                plugin.on_decision_made(decision)

    def halt(self):
        """
        Stop the Framer from processing further actions and tasks.
        """
        self.acting = False
        self.can_execute = False
        logger.info("Framer halted. No further actions or tasks will be processed.")

    async def generate_tasks_from_perception(
        self,
        perception: Union[Perception, Dict[str, Any]],
        max_len: Optional[int] = None,
    ) -> List[Task]:
        """
        Generate tasks based on the given perception.

        Args:
            perception (Union[Perception, Dict[str, Any]]): The perception to generate tasks from.
            max_len (Optional[int]): Maximum number of tasks to generate. If None, no limit is applied.

        Returns:
            List[Task]: A list of generated tasks.
        """
        tasks = []

        # Convert dictionary to Perception object if necessary
        if isinstance(perception, dict):
            perception = Perception.from_dict(perception)

        # Example: Create a task to process the perception
        task = Task(
            description=f"Process perception of type: {perception.type}",
            workflow_id="perception_processing",
        )
        tasks.append(task)

        # Add more sophisticated logic here to generate tasks based on the perception content
        # For example, you could analyze the perception data and create specific tasks

        # Limit the number of tasks if max_len is specified
        if max_len is not None:
            tasks = tasks[:max_len]

        return tasks

    async def close(self) -> None:
        """
        Optimize and clear all memory for the Framer.

        This method ensures that all tasks and workflows are closed properly,
        and any resources or memory used by the Framer are released. It is
        important to call this method when the Framer is no longer needed to
        prevent memory leaks and ensure optimal performance. This method
        should be called to gracefully shut down the Framer.
        """
        # Close all workflows
        for workflow in self.workflow_manager.workflows.values():
            workflow.set_final_task(
                Task(description="Final Task")
            )  # Set a default final task
            for task in workflow.tasks:
                task.update_status(TaskStatus.COMPLETED)  # Mark tasks as completed

        # Clear memory
        if self.memory_service and hasattr(self.memory_service, "clear"):
            self.memory_service.clear()

        # Notify observers and plugins about closure and opening
        for observer in self.observers:
            if hasattr(observer, "on_framer_closed"):
                observer.on_framer_closed(self)

        if hasattr(self, "plugins"):
            for plugin in self.plugins.values():
                if hasattr(plugin, "on_framer_closed"):
                    plugin.on_framer_closed(self)

        # Ensure plugins are properly shut down
        for plugin in self.plugins.values():
            if hasattr(plugin, "on_shutdown"):
                # Await on_shutdown if it's a coroutine
                if asyncio.iscoroutinefunction(plugin.on_shutdown):
                    await plugin.on_shutdown()
                else:
                    plugin.on_shutdown()
