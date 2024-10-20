import asyncio
import logging
import time
import json
import importlib
from typing import List, Dict, Any, Optional, Callable, Union, Tuple, Deque
from collections import deque
from frame.src.services.llm.main import LLMService
from frame.src.services.context.shared_context_service import SharedContext
from frame.src.framer.config import FramerConfig
from frame.src.framer.agency import Agency
from frame.src.framer.brain import Brain
from frame.src.framer.soul import Soul
from frame.src.framer.agency.workflow import WorkflowManager
from frame.src.framer.agency.tasks.task import Task
from frame.src.models.framer.agency.tasks import TaskStatus
from frame.src.utils.config_parser import (
    parse_json_config,
    parse_markdown_config,
    export_config_to_markdown,
)
from frame.src.utils.llm_utils import (
    get_completion,
    choose_best_model_for_tokens,
)
from frame.src.utils.token_utils import calculate_token_size
from frame.src.framer.brain.perception import Perception
from frame.src.framer.brain.decision import Decision
from frame.src.services.llm.llm_adapters.dspy.dspy_adapter import DSPyAdapter
from frame.src.services import MemoryService
from frame.src.framer.brain.memory.memory_adapter_interface import MemoryAdapterInterface
from frame.src.services import EQService
from frame.src.utils.metrics import MetricsManager
from frame.src.services import ExecutionContext
from frame.src.framer.agency.goals import GoalStatus
from frame.src.framer.brain.memory.memory_adapters.mem0_adapter import Mem0Adapter

Observer = Callable[[Decision], None]

logger = logging.getLogger("frame.framer")


class Framer:
    perceptions_queue: Deque[Union[Perception, Dict[str, Any]]] = deque()
    """
    The Framer class represents an AI agent with cognitive capabilities. It integrates various components
    such as agency, brain, soul, and workflow management to create a comprehensive AI entity capable of
    processing perceptions, making decisions, and executing tasks.

    Attributes:
        config (FramerConfig): Configuration settings for the Framer.
        llm_service (LLMService): The language model service to be used by the Framer.
        agency (Agency): Manages roles, goals, tasks, and workflows for the Framer.
        brain (Brain): Handles decision-making processes, integrating perceptions, memories, and thoughts.
        soul (Soul): Represents the core essence and personality of a Framer.
        workflow_manager (WorkflowManager): Manages workflows and tasks.
        memory_service (Optional[MemoryService]): Service for managing memory. Default is None.
        eq_service (Optional[EQService]): Service for managing emotional intelligence. Default is None.
        roles (Optional[List[Dict[str, Any]]]): List of roles for the Framer. Default is None.
        goals (Optional[List[Dict[str, Any]]]): List of goals for the Framer. Default is None.
        observers (List[Observer]): List of observer functions to notify on decisions.
        can_execute (bool): Determines if decisions are executed automatically. Default is True.
        acting (bool): Indicates if the Framer is actively processing perceptions. Default is False.
    """

    def __init__(
        self,
        config: FramerConfig,
        llm_service: LLMService,
        agency: Agency,
        brain: Brain,
        soul: Soul,
        workflow_manager: WorkflowManager,
        memory_adapter: Optional[MemoryAdapterInterface] = None,
        memory_service: Optional[MemoryService] = None,
        eq_service: Optional[EQService] = None,
        roles: List[Dict[str, Any]] = [],
        goals: List[Dict[str, Any]] = [],
        plugins: Optional[Dict[str, Any]] = None,
        plugin_loading_progress: Optional[Callable[[int], None]] = None,
    ):
        self.plugin_loading_progress = plugin_loading_progress
        # Existing initialization code...

        self.config = config
        self.permissions = config.permissions or ["with_memory", "with_mem0_search_extract_summarize_plugin", "with_shared_context"]

        # Initialize services and plugins based on permissions
        # Services like memory, eq, and shared_context are special plugins called services.
        # They do not require explicit permissions to be accessed but must be passed into a Framer.
        # The Mem0SearchExtractSummarizePlugin is a default plugin that provides a response mechanism
        # requiring memory retrieval, functioning as a RAG mechanism.
        # Enforce permission for 'with-mem0-search-extract-summarize-plugin' if 'with-memory' is used
        if "with-memory" in self.permissions:
            self.permissions.append("with-mem0-search-extract-summarize-plugin")
        
        if "with-memory" in self.permissions and memory_adapter:
            self.memory_service = memory_service or MemoryService(adapter=memory_adapter)

        if "with_eq" in self.permissions:
            self.eq_service = eq_service or EQService()

        if "with_shared_context" in self.permissions:
            self.shared_context_service = SharedContext()

        self.config = config
        self.llm_service = llm_service
        self.agency = agency
        self.brain = brain
        self.soul = soul
        self.workflow_manager = workflow_manager
        self.memory_service = memory_service
        self.roles = roles
        self.goals = goals
        self.eq_service = eq_service
        self.plugins = plugins or {}
        self.plugin_loading_complete = False
        self._streamed_response = {"status": "pending", "result": ""}
        self.config = config
        self.llm_service = llm_service
        self.agency = agency
        self.brain = brain
        self.soul = soul
        self.workflow_manager = workflow_manager
        self.memory_service = memory_service
        self.eq_service = eq_service
        self._dynamic_model_choice = False
        self.observers: List[Observer] = []
        self.can_execute = True  # Add can_execute attribute
        self.acting = False
        # Load plugins asynchronously
        asyncio.create_task(self.load_plugins())

    def act(self):
        """
        Enable the Framer to start acting and processing perceptions.
        """
        self.acting = True
            
    async def load_plugins(self):
        """
        Load all plugins by calling their on_load method.
        """
        for plugin_name, plugin_instance in self.plugins.items():
            if hasattr(plugin_instance, "on_load"):
                await plugin_instance.on_load(self)
                # Register plugin actions
                for action_name, action_func in plugin_instance.get_actions().items():
                    self.agency.action_registry.add_action(
                        action_name,
                        action_func=action_func,
                        description=f"Action from {plugin_name} plugin",
                        priority=5  # Default priority, adjust as needed
                    )
        self.plugin_loading_complete = True
        self.act()
        await self.process_queued_perceptions()

    async def process_queued_perceptions(self):
        """
        Process all queued perceptions once the Framer is ready.
        """
        if self.is_ready():
            logger.info("Processing queued perceptions...")
            while self.perceptions_queue:
                logger.info(f"Processing perception from queue: {self.perceptions_queue[0]}")
                perception = self.perceptions_queue.popleft()
                await self.sense(perception)

            if not self.roles and not self.goals:
                self.roles, self.goals = await self.agency.generate_roles_and_goals()
            elif not self.roles:
                self.roles, _ = await self.agency.generate_roles_and_goals()
            elif not self.goals:
                _, self.goals = await self.agency.generate_roles_and_goals()

            # Sort roles and goals by priority
            self.roles.sort(key=lambda x: x.get("priority", 5), reverse=True)
            self.goals.sort(key=lambda x: x.get("priority", 5), reverse=True)

            self.agency.set_roles(self.roles)
            self.agency.set_goals(self.goals)
        else:
            logger.warning("Framer is not ready. Queuing perception.")
            logger.info(f"Queued perception: {perception}")

        # Sort roles and goals by priority
        self.roles.sort(key=lambda x: x.get("priority", 5), reverse=True)
        self.goals.sort(key=lambda x: x.get("priority", 5), reverse=True)

        self.agency.set_roles(self.roles)
        self.agency.set_goals(self.goals)

    async def export_to_file(self, file_path: str, llm) -> None:
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
        return cls(
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

    def export_to_markdown(self, file_path: str) -> None:
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

    async def use_plugin_action(self, plugin_name: str, action_name: str, parameters: Dict[str, Any]) -> Any:
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

    async def sense(self, perception: Union[Perception, Dict[str, Any]]) -> Optional[Decision]:
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
        """
        Process a perception and make a decision.

        Args:
            perception (Union[Perception, Dict[str, Any]]): The perception to process, can be a Perception object or a dictionary.

        Returns:
            Decision: The decision made based on the perception.
        """
        if not self.plugin_loading_complete or not self.acting:
            logger.warning("Framer is not ready. Queuing perception.")
            self.perceptions_queue.append(perception)
            return None  # Return None to indicate the perception was queued
        # Convert perception to Perception object if it is a dictionary
        if isinstance(perception, dict):
            perception = Perception.from_dict(perception)
        current_goals = self.agency.get_goals()
        decision = await self.brain.process_perception(perception, current_goals)

        # Consider goal status in decision-making
        active_goals = [
            goal for goal in current_goals if goal.status == GoalStatus.ACTIVE
        ]
        if active_goals:
            decision.reasoning += f" (Aligned with {len(active_goals)} active goals)"

        if hasattr(self, "can_execute") and self.can_execute:
            await self.brain.execute_decision(decision)
        logger.debug(f"Processed perception: {perception}, Decision: {decision}")
        self.notify_observers(decision)
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
