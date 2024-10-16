import logging
import time
from typing import List, Dict, Any, Optional, Callable, Union
from frame.src.services.llm.main import LLMService
from frame.src.framer.config import FramerConfig
from frame.src.framer.agency import Agency
from frame.src.framer.brain import Brain
from frame.src.framer.soul import Soul
from frame.src.framer.agency.tasks.workflow.workflow_manager import WorkflowManager
from frame.src.framer.agency.tasks.task import Task
from frame.src.utils.config_parser import load_framer_from_file, export_config_to_markdown
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

    @classmethod
    def load_from_file(cls, file_path: str, llm_service: LLMService, memory_service: Optional[MemoryService] = None, eq_service: Optional[EQService] = None) -> "Framer":
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
        config = load_framer_from_file(file_path)
        return cls(config=config, llm_service=llm_service, agency=Agency(llm_service=llm_service, context=None), brain=Brain(llm_service=llm_service, default_model=config.default_model, roles=config.roles, goals=config.goals, soul=Soul(seed=config.soul_seed)), soul=Soul(seed=config.soul_seed), workflow_manager=WorkflowManager(), memory_service=memory_service, eq_service=eq_service, roles=config.roles, goals=config.goals)

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

    def export_to_json(self, file_path: str) -> None:
        """
        Export the Framer configuration to a JSON file.

        This method allows the Framer agent to be fully exported into a JSON format,
        making it portable and easy to use inside a prompt to any other LLM. This
        portability enables the Framer agents to be shared and consumed by other
        systems, facilitating interoperability and reuse.

        Args:
            file_path (str): The path to the file where the JSON will be saved.
        """
        import json
        with open(file_path, 'w') as file:
            json.dump({
                "config": self.config.to_dict(),
                "roles": self.roles,
                "goals": self.goals
            }, file, indent=4)

    @classmethod
    def load_from_file(cls, file_path: str, llm_service: LLMService, memory_service: Optional[MemoryService] = None, eq_service: Optional[EQService] = None) -> "Framer":
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
        config = load_framer_from_file(file_path)
        return cls(config=config, llm_service=llm_service, agency=Agency(llm_service=llm_service, context=None), brain=Brain(llm_service=llm_service, default_model=config.default_model, roles=config.roles, goals=config.goals, soul=Soul(seed=config.soul_seed)), soul=Soul(seed=config.soul_seed), workflow_manager=WorkflowManager(), memory_service=memory_service, eq_service=eq_service, roles=config.roles, goals=config.goals)

    def export_to_json(self, file_path: str) -> None:
        """
        Export the Framer configuration to a JSON file.

        This method allows the Framer agent to be fully exported into a JSON format,
        making it portable and easy to use inside a prompt to any other LLM. This
        portability enables the Framer agents to be shared and consumed by other
        systems, facilitating interoperability and reuse.

        Args:
            file_path (str): The path to the file where the JSON will be saved.
        """
        import json
        with open(file_path, 'w') as file:
            json.dump({
                "config": self.config.to_dict(),
                "roles": self.roles,
                "goals": self.goals
            }, file, indent=4)

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
