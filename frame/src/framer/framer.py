import logging
import time
from typing import List, Dict, Any, Optional, Callable
from frame.src.services.llm.main import LLMService
from frame.src.framer.config import FramerConfig
from frame.src.framed.config import FramedConfig
from frame.src.framer.agency import Agency
from frame.src.framer.brain import Brain
from frame.src.framer.soul import Soul
from frame.src.framer.agency.tasks.workflow.workflow_manager import WorkflowManager
from frame.src.framer.agency.tasks.task import Task
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

Observer = Callable[[Decision], None]

logger = logging.getLogger("frame.framer")


class Framer:
    def __init__(
        self,
        config: FramedConfig,
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
        if config.default_model and config.default_model != "gpt-3.5-turbo":
            self.llm_service.set_default_model(config.default_model)
        self.agency = agency
        self.brain = brain
        self.soul = soul
        self.workflow_manager = workflow_manager
        self.memory_service = memory_service
        self.eq_service = eq_service
        self._dynamic_model_choice = False
        self.observers = []
        self.can_execute = True  # Add can_execute attribute

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
        soul_seed: Optional[Dict[str, str]] = None,
        memory_service: Optional[MemoryService] = None,
        eq_service: Optional[EQService] = None,
    ) -> "Framer":
        agency = Agency(llm_service=llm_service, context=None)

        # Generate roles and goals if they are None or empty lists
        roles = config.roles
        goals = config.goals

        if roles is None and goals is None:
            roles, goals = await agency.generate_roles_and_goals()
        elif roles == [] and goals is None:
            roles, _ = await agency.generate_roles_and_goals()
        elif goals == [] and roles is None:
            _, goals = await agency.generate_roles_and_goals()
        elif roles == [] and goals == []:
            roles, goals = await agency.generate_roles_and_goals()

        brain = Brain(
            llm_service=llm_service,
            default_model=config.default_model,
            roles=roles,
            goals=goals,
        )
        soul = Soul(seed=soul_seed if soul_seed else {"seed": "default"})
        workflow_manager = WorkflowManager()

        return cls(
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

    async def initialize(self):
        if not self.agency.roles:
            self.agency.roles, self.agency.goals = (
                await self.agency.generate_roles_and_goals()
            )

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
        soul_seed (Optional[Dict[str, str]]): Initial seed for the Framer's soul.
        memory_service (Optional[MemoryService]): Memory service for the Framer.
        eq_service (Optional[EQService]): Emotional intelligence service for the Framer.

    Returns:
        Framer: A new Framer instance.
    """

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
