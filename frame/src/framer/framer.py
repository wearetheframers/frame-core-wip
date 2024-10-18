import logging
import time
import json
import importlib
from typing import List, Dict, Any, Optional, Callable, Union, Tuple
from frame.src.services import LLMService, SharedContext
from frame.src.framer.config import FramerConfig
from frame.src.framer.agency import Agency
from frame.src.framer.brain import Brain
from frame.src.framer.soul import Soul
from frame.src.framer.agency.tasks.workflow.workflow_manager import WorkflowManager
from frame.src.framer.agency.tasks.task import Task
from frame.src.models.framer.agency.tasks.task import TaskStatus
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
from frame.src.services import EQService
from frame.src.utils.metrics import MetricsManager
from frame.src.services import ExecutionContext
from frame.src.models.framer.agency.goals import GoalStatus
from frame.src.framer.brain.memory.memory_adapters.mem0_adapter import Mem0Adapter

Observer = Callable[[Decision], None]

logger = logging.getLogger("frame.framer")


class Framer:
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
        memory_service: Optional[MemoryService] = None,
        eq_service: Optional[EQService] = None,
        roles: List[Dict[str, Any]] = [],
        goals: List[Dict[str, Any]] = [],
    ):
        # Existing initialization code...

        self.config = config
        self.permissions = config.permissions

        # Initialize services and plugins based on permissions
        if "withMemory" in self.permissions:
            self.memory_service = memory_service or MemoryService()
        
        if "withEQ" in self.permissions:
            self.eq_service = eq_service or EQService()
        
        if "withSharedContext" in self.permissions:
            self.shared_context_service = SharedContext()

        # Initialize custom plugins
        self.plugins = {}
        for permission in self.permissions:
            if permission.startswith("with") and permission not in ["withMemory", "withEQ", "withSharedContext"]:
                plugin_name = permission[4:]  # Remove 'with' prefix
                try:
                    plugin_module = importlib.import_module(f"frame.src.plugins.{plugin_name.lower()}")
                    plugin_class = getattr(plugin_module, plugin_name)
                    self.plugins[plugin_name] = plugin_class(self)
                except ImportError:
                    self.logger.warning(f"{plugin_name} is not available. To use it, install the required dependencies.")

        # Initialize Mem0Adapter if API key is provided and permission is granted
        if config.mem0_api_key and "withMemory" in self.permissions:
            self.mem0_adapter = Mem0Adapter(api_key=config.mem0_api_key)
        else:
            self.mem0_adapter = None
            self.logger.warning("Mem0 API key not provided or permission not granted. Mem0Adapter will not be available.")
        """
        Initialize a Framer instance.

        Args:
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
        """
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
        self.plugins: Dict[str, Any] = {}  # Initialize plugins attribute
        self.can_execute = True  # Add can_execute attribute
        self.acting = False

        # Initialize roles and goals
        self.roles: List[Dict[str, Any]] = roles if roles is not None else []
        self.goals: List[Dict[str, Any]] = goals if goals is not None else []
        self.act()

    @classmethod
    async def create(
        cls,
        config: FramerConfig,
        llm_service: LLMService,
        soul_seed: Optional[Union[str, Dict[str, Any]]] = None,
        memory_service: Optional[MemoryService] = None,
        eq_service: Optional[EQService] = None,
    ) -> "Framer":
        agency = Agency(llm_service=llm_service, context={}, execution_context=None)

        # Generate roles and goals if they are None
        roles = config.roles
        goals = config.goals

        soul = Soul(seed=config.soul_seed)
        brain = Brain(
            llm_service=llm_service,
            default_model="gpt-4o",
            roles=roles,
            goals=goals,
            soul=soul,
        )
        workflow_manager = WorkflowManager()

        framer = cls(
            config=config,
            llm_service=llm_service,
            agency=agency,
            brain=brain,
            soul=soul,
            workflow_manager=workflow_manager,
            memory_service=memory_service,
            eq_service=eq_service,
            roles=roles,
            goals=goals,
        )

        await framer.initialize(
            llm_service=llm_service,
            memory_service=memory_service,
            eq_service=eq_service,
        )
        # Notify observers about the Framer being opened
        for observer in framer.observers:
            if hasattr(observer, "on_framer_opened"):
                observer.on_framer_opened(framer)

        return framer

    def act(self):
        """
        Enable the Framer to process perceptions and make decisions.

        This method sets the Framer to an active state, allowing it to respond
        to perceptions and execute tasks. It is automatically called during
        initialization to ensure the Framer starts acting immediately.
        """
        self.acting = True

    async def initialize(self):
        """Initialize the Framer with roles and goals."""

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

        # Load the SearchExtractSummarizePlugin
        await self.search_extract_summarize_plugin.on_load()

        self.act()  # Start acting after initialization

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

    async def sense(self, perception: Union[Perception, Dict[str, Any]]) -> Decision:
        """
        Process a perception and make a decision.

        Args:
            perception (Union[Perception, Dict[str, Any]]): The perception to process, can be a Perception object or a dictionary.

        Returns:
            Decision: The decision made based on the perception.
        """
        if not self.acting:
            logger.warning("Framer is not acting. Cannot process perceptions.")
            return Decision(
                action="error", parameters={}, reasoning="Framer is halted."
            )
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
        return decision  # Return the Decision object directly

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
