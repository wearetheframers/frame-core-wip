import logging
import time
from typing import List, Dict, Any, Optional, Callable, Union
from frame.src.services.llm.main import LLMService
from frame.src.framer.config import FramerConfig
from frame.src.framed.config import FramedConfig
from frame.src.framer.agency import Agency
from frame.src.framer.brain import Brain
from frame.src.framer.soul import Soul
from frame.src.framer.agency.tasks.workflow.workflow_manager import WorkflowManager
from frame.src.framer.agency.tasks.task import Task
from frame.src.utils.config_parser import load_framer_from_file, export_framer_to_json, export_framer_to_markdown
from frame.src.utils.llm_utils import (
    get_completion,
    calculate_token_size,
    choose_best_model_for_tokens,
)
from frame.src.framer.brain.perception import Perception
from frame.src.framer.brain.decision import Decision
from frame.src.services.llm.llm_adapters.dspy.dspy_adapter import DSPyAdapter
from frame.src.services.memory.main import MemoryService
from frame.src.services.eq.main import EQService
from frame.src.utils.metrics import MetricsManager
from frame.src.framer.agency.execution_context import ExecutionContext

Observer = Callable[[Decision], None]

logger = logging.getLogger("frame.framer")


class Framer:
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
        roles: Optional[List[Dict[str, Any]]] = None,
        goals: Optional[List[Dict[str, Any]]] = None,
    ):
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
        self.observers = []
        self.can_execute = True  # Add can_execute attribute

        # Initialize roles and goals
        self.roles = roles
        self.goals = goals

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
        if hasattr(self, "plugins"):
            for plugin in self.plugins.values():
                if hasattr(plugin, "on_decision_made"):
                    plugin.on_decision_made(decision)

    def notify_task_completion(self, task: Task) -> None:
        """
        Notify all observers and plugins about task completion.

        Args:
            task (Task): The task that was completed.
        """
        for observer in self.observers:
            if hasattr(observer, "on_task_completed"):
                observer.on_task_completed(task)

        if hasattr(self, "plugins"):
            for plugin in self.plugins.values():
                if hasattr(plugin, "on_task_completed"):
                    plugin.on_task_completed(task)

    @classmethod
    async def create(
        cls,
        config: FramerConfig,
        llm_service: LLMService,
        soul_seed: Optional[Union[str, Dict[str, Any]]] = None,
        memory_service: Optional[MemoryService] = None,
        eq_service: Optional[EQService] = None,
    ) -> "Framer":
        agency = Agency(llm_service=llm_service, context=None)

        # Generate roles and goals if they are None
        roles = config.roles
        goals = config.goals

        soul = Soul(seed=soul_seed)
        brain = Brain(
            llm_service=llm_service,
            default_model=config.default_model,
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

        await framer.initialize()
        return framer

    async def initialize(self):
        """
        Initialize the Framer by generating or updating roles and goals.

        This method ensures that the Framer has valid roles and goals:
        1. If both roles and goals are None, generate new roles and goals.
        2. If roles are an empty list, set both roles and goals to empty lists.
        3. If goals are None and roles are provided (not None or empty), generate new goals.
        4. If both roles and goals are provided (not None), use the provided values.
        """
        if self.roles is None and self.goals is None:
            generated_roles, generated_goals = (
                await self.agency.generate_roles_and_goals()
            )
            self.roles = [
                {"name": role, "description": f"{role} description"}
                for role in generated_roles
            ]
            self.goals = [
                {"description": goal, "priority": 1} for goal in generated_goals
            ]
        elif self.roles == []:
            self.goals = []
        elif self.goals is None and self.roles:
            _, generated_goals = await self.agency.generate_roles_and_goals()
            self.goals = [
                {"description": goal, "priority": 1} for goal in generated_goals
            ]
        elif self.roles and self.goals is None:
            new_roles, _ = await self.agency.generate_roles_and_goals()
            self.roles.extend(
                [
                    {"name": role, "description": f"{role} description"}
                    for role in new_roles
                ]
            )

        if not self.roles:
            self.roles = [
                {"name": "Default Role", "description": "Default role description"}
            ]
        if not self.goals:
            self.goals = [
                {
                    "description": "Assist users to the best of my abilities",
                    "priority": 1,
                }
            ]

        self.agency.set_roles(self.roles)
        self.agency.set_goals(self.goals)

        # Ensure the agency has the roles and goals attributes
        self.agency.roles = self.roles
        self.agency.goals = self.goals

    # Add a docstring explaining the role and goal generation behavior
    create.__doc__ = """
    Create a new Framer instance.

    Role and goal generation behavior:
    - If both roles and goals are None, they will be generated using generate_roles_and_goals().
    - If roles is an empty list [] and goals is None, only roles will be generated.
    - If goals is an empty list [] and roles is None, only goals will be generated.
    - If both roles and goals are empty lists [], both will be generated.
    - If either roles or goals is provided (not None or empty list), the provided value will be used.

    Args:
        config (FramerConfig): Configuration for the Framer.
        llm_service (LLMService): Language model service.
        soul_seed (Optional[Union[str, Dict[str, Any]]]): Initial seed for the Framer's soul.
            Can be either a string or a dictionary. If a string is provided, it will be used
            as the 'text' value in the soul's seed dictionary. If a dictionary is provided,
            it can include any keys and values, with an optional 'text' key for the soul's essence.
        memory_service (Optional[MemoryService]): Memory service for the Framer.
        eq_service (Optional[EQService]): Emotional intelligence service for the Framer.

    Returns:
        Framer: A new Framer instance.
    """

    @classmethod
    def load_from_file(cls, file_path: str, llm_service: LLMService, memory_service: Optional[MemoryService] = None, eq_service: Optional[EQService] = None) -> "Framer":
        config = load_framer_from_file(file_path)
        return cls(config=config, llm_service=llm_service, agency=Agency(llm_service=llm_service, context=None), brain=Brain(llm_service=llm_service, default_model=config.default_model, roles=config.roles, goals=config.goals, soul=Soul(seed=config.soul_seed)), soul=Soul(seed=config.soul_seed), workflow_manager=WorkflowManager(), memory_service=memory_service, eq_service=eq_service, roles=config.roles, goals=config.goals)

    def export_to_json(self, file_path: str) -> None:
        export_framer_to_json(self, file_path)

    async def perform_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform a task asynchronously.

        Args:
            task (Dict[str, Any]): Dictionary containing task details.

        Returns:
            Dict[str, Any]: Result of the task execution.
        """
        logger.debug(f"perform_task called with task: {task}")
        task_obj = Task(**task)
        result = await self.agency.perform_task(task_obj)
        return result if result is not None else {"output": "No result returned"}

    async def sense(self, perception: Any) -> Decision:
        """
        Process a perception and make a decision.

        Args:
            perception (Any): The perception to process, can be a Perception object or a dictionary.

        Returns:
            Decision: The decision made based on the perception.
        """
        if isinstance(perception, dict):
            perception = Perception.from_dict(perception)
        decision = await self.brain.process_perception(
            perception, self.agency.get_goals()
        )
        if hasattr(self, "can_execute") and self.can_execute:
            await self.brain.execute_decision(decision)
        logger.debug(f"Processed perception: {perception}, Decision: {decision}")
        self.notify_observers(decision)
        return decision
