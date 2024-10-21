from typing import List, Dict, Any, Optional, Tuple, Union
import json
import logging
import time

from frame.src.constants.models import DEFAULT_MODEL
from .priority import Priority
from .roles import RoleStatus
from .tasks import Task, TaskStatus
from .workflow import WorkflowManager, Workflow
from .roles import Role
from .goals import Goal
from frame.src.framer.agency.goals import GoalStatus
from frame.src.services.llm import LLMService
from frame.src.services.execution_context import ExecutionContext
from frame.src.framer.brain.decision import Decision
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from frame.src.framer.brain.brain import Brain

logger = logging.getLogger(__name__)


class Agency:
    """
    The Agency class manages task execution, decision-making, and role/goal coordination for a Framer.

    It orchestrates complex operations by managing roles, goals, tasks, and workflows. The Agency
    supports concurrent execution of multiple roles, goals, and tasks, enabling sophisticated
    and multi-faceted behavior.

    Key features:
    - Multi-role and multi-goal support
    - Concurrent task execution
    - Dynamic workflow management
    - Decision-making based on context, roles, and goals
    - LLM integration for task execution and decision-making

    Attributes:
        execution_context (ExecutionContext): Contains necessary services and state.
        roles (List[Role]): Active roles assigned to the Agency.
        goals (List[Goal]): Active goals for the Agency.
        workflow_manager (WorkflowManager): Manages workflows and tasks.
        framer (Framer): The associated Framer instance.
        llm_service (LLMService): Language model service for text generation.
        context (Dict[str, Any]): Additional context information.
        default_model (str): Default language model for text generation.
    """

    def __init__(
        self,
        llm_service: LLMService,
        execution_context: Optional[ExecutionContext] = None,
        roles: Optional[List[Role]] = [],
        goals: Optional[List[Goal]] = [],
        context: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize an Agency instance.

        Args:
            llm_service (LLMService): The language model service.
            context (Optional[Dict[str, Any]]): Additional context for the Agency. Defaults to None.
            roles (Optional[List[Role]]): Initial roles for the Agency. Defaults to None.
            goals (Optional[List[Goal]]): Initial goals for the Agency. Defaults to None.
        """
        self.llm_service = llm_service
        self.execution_context = execution_context or ExecutionContext()
        self.roles: List[Role] = []
        self.goals: List[Goal] = []
        if roles:
            self.set_roles(roles)
        if goals:
            self.set_goals(goals)
        self.workflow_manager = WorkflowManager()
        self.completion_calls = {}
        self.default_model = getattr(self.llm_service, "default_model", DEFAULT_MODEL)

    def set_roles(self, roles: Optional[List[Role]] = None) -> None:
        self.roles = roles if roles is not None else []

    def set_goals(self, goals: Optional[List[Goal]] = None) -> None:
        self.goals = goals if goals is not None else []

    def get_roles(self) -> List[Role]:
        return self.roles

    def get_goals(self) -> List[Goal]:
        return [goal for goal in self.goals if goal.status == GoalStatus.ACTIVE]

    def create_task(
        self,
        description: str,
        priority: Union[str, Priority] = Priority.MEDIUM,
        workflow_id: str = "default",
    ) -> Task:
        """
        Create a new task with the given description and priority.

        Args:
            description (str): The description of the task.
            priority (Union[str, Priority], optional): The priority of the task. Can be a string or Priority enum. Defaults to Priority.MEDIUM.
            workflow_id (str, optional): The ID of the workflow this task belongs to. Defaults to "default".

        Returns:
            Task: The created Task object.
        """
        if isinstance(priority, str):
            priority = Priority.get(priority)
        elif not isinstance(priority, Priority):
            raise ValueError("Priority must be a string or Priority enum")
        return Task(description=description, priority=priority, workflow_id=workflow_id)

    def add_task(self, task: Task, workflow_id: str = "default") -> None:
        """
        Add a new task to a specified workflow.

        Args:
            task (Task): The task to add.
            workflow_id (str, optional): The ID of the workflow to add the task to. Defaults to "default".
        """
        # Ensure the workflow exists before adding a task
        if not self.workflow_manager.get_workflow(workflow_id):
            self.workflow_manager.create_workflow(workflow_id)
        self.workflow_manager.add_task(workflow_id, task)

    def get_next_task(self, workflow_id: str = "default") -> Optional[Task]:
        """
        Get the next pending task with the highest priority from a specified workflow.

        Args:
            workflow_id (str, optional): The ID of the workflow to get the task from. Defaults to "default".

        Returns:
            Optional[Task]: The next task to be executed, or None if no pending tasks.
        """
        workflow = self.workflow_manager.get_workflow(workflow_id)
        if workflow is None:
            return None
        pending_tasks = [
            task for task in workflow.tasks if task.status == TaskStatus.PENDING
        ]
        return (
            max(pending_tasks, key=lambda task: task.priority)
            if pending_tasks
            else None
        )

    def complete_task(self, task: Task, result: Any) -> None:
        """
        Mark a task as completed and set its result.

        Args:
            task (Task): The task to be marked as completed.
            result (Any): The result of the completed task.
        """
        task.update_status(TaskStatus.COMPLETED)
        task.set_result(result)

    def fail_task(self, task: Task, reason: str) -> None:
        """
        Mark a task as failed and set the failure reason.

        Args:
            task (Task): The task to be marked as failed.
            reason (str): The reason for the task failure.
        """
        task.update_status(TaskStatus.FAILED)
        task.set_result(reason)

    def create_workflow(self, name: str, is_async: bool = False) -> Workflow:
        """
        Create a new workflow.

        Args:
            name (str): The name of the workflow.
            is_async (bool, optional): Whether the workflow is asynchronous. Defaults to False.

        Returns:
            Workflow: The created Workflow object.
        """
        return self.workflow_manager.create_workflow(name, is_async)

    def set_final_task_for_workflow(self, workflow_name: str, task: Task) -> None:
        """
        Set the final task for a specified workflow.

        Args:
            workflow_name (str): The name of the workflow.
            task (Task): The task to be set as the final task.
        """
        self.workflow_manager.set_final_task_for_workflow(workflow_name, task)

    def get_all_tasks(self) -> List[Dict[str, Any]]:
        """
        Get all tasks from all workflows.

        Returns:
            List[Dict[str, Any]]: A list of all tasks as dictionaries.
        """
        all_tasks = []
        for workflow in self.workflow_manager.workflows.values():
            all_tasks.extend([task.to_dict() for task in workflow.tasks])
        return all_tasks

    async def perform_task(self, task: Union[Dict[str, Any], Task]) -> Dict[str, Any]:
        """
        Perform a task asynchronously.

        Args:
            task (Union[Dict[str, Any], Task]): Dictionary containing task details or a Task object.

        Returns:
            Dict[str, Any]: Result of the task execution.
        """
        logger.debug(f"perform_task called with task: {task}")
        if isinstance(task, Task):
            task_obj = task
        else:
            task_dict = task.copy()
            if "workflow_id" not in task_dict:
                task_dict["workflow_id"] = "default"
            task_obj = Task(**task_dict)
        result = await self._perform_task(task_obj)
        return result if result is not None else {"output": "No result returned"}

    async def _perform_task(self, task: Task) -> Dict[str, Any]:
        """
        Internal method to perform a task asynchronously.

        Args:
            task (Task): Task object to be performed.

        Returns:
            Dict[str, Any]: Result of the task execution.
        """
        logger.debug(f"_perform_task called with task: {task.description}")
        start_time = time.time()

        if task.workflow_id not in self.completion_calls:
            self.completion_calls[task.workflow_id] = {}
        if task.id not in self.completion_calls[task.workflow_id]:
            self.completion_calls[task.workflow_id][task.id] = 0

        # Perform the task
        priority_explanation = """
        Priority levels are defined as follows:
        1 - LOWEST
        2 - VERY LOW
        3 - LOW
        4 - MEDIUM LOW
        5 - MEDIUM
        6 - MEDIUM HIGH
        7 - HIGH
        8 - VERY HIGH
        9 - HIGHEST
        10 - CRITICAL

        When making decisions, prioritize tasks with higher priority levels, but introduce some variability to avoid always selecting the same task. Consider the context and relevance of each task to determine the best course of action.
        """

        prompt = f"""
        Execute the following task: {task.description}

        {priority_explanation}

        Consider the context and relevance of each task, and introduce some variability in your decision-making process.
        """
        response = await self.llm_service.get_completion(
            prompt,
            model=self.default_model,
            max_tokens=200,
            temperature=0.7,
        )

        # Update task status and result
        task.update_status(TaskStatus.COMPLETED)
        task.set_result(response)

        # Log task completion
        end_time = time.time()
        duration = end_time - start_time
        logger.debug(f"Task '{task.description}' completed in {duration:.2f} seconds.")
        logger.debug(f"Task result: {response}")

        return {"output": response}

    async def generate_roles(self) -> List[Role]:
        """
        Generate roles based on the Framer's context.

        Returns:
            List[RoleModel]: A list of generated roles.
        """
        soul = getattr(self.execution_context, "soul", {})
        prompt = f"""Generate a role that aligns with the Framer's current context. 
        The role should be clear, relevant, and directly related to the given information.
        Avoid creating complex scenarios. Keep it simple and focused.
        
        Soul: {json.dumps(soul, indent=2)}
        
        Respond with a JSON object containing 'id', 'name', 'description', 'permissions', 'priority', and 'status' fields for the role.
        Ensure the priority is an integer between 1 and 10, where 10 is the highest priority.
        The status should be one of: 'ACTIVE', 'INACTIVE', or 'SUSPENDED'.
        Consider the importance and urgency of the role when assigning the priority and status."""
        logger.debug(f"Role generation prompt: {prompt}")
        try:
            response = await self.llm_service.get_completion(
                prompt, model=self.default_model, max_tokens=150, temperature=0.5
            )
            logger.debug(f"Role generation response: {response}")
            if response is None:
                logger.warning(
                    "Received None response while generating role. Using default role."
                )
                return [
                    Role(
                        id="default",
                        name="Task Assistant",
                        description="Assist with the given task or query.",
                        priority=5,
                        status=RoleStatus.ACTIVE,
                    )
                ]
            role_data = json.loads(response)
            if not role_data:
                logger.warning(
                    "Received empty response while generating role. Using default role."
                )
                return [
                    Role(
                        id="default",
                        name="Task Assistant",
                        description="Assist with the given task or query.",
                        priority=5,
                        status=RoleStatus.ACTIVE,
                    )
                ]

            if isinstance(role_data, dict):
                role_data = [role_data]

            roles = []
            existing_role_names = set()
            for r in role_data:
                r["priority"] = max(1, min(10, int(r.get("priority", 5))))
                r["status"] = RoleStatus[r.get("status", "ACTIVE")]
                # Ensure permissions are a list
                r["permissions"] = list(r.get("permissions", []))
                if r["name"] not in existing_role_names:
                    roles.append(Role(**r))
                    existing_role_names.add(r["name"])
                    logger.info(f"Generated unique role: {r['name']}")
                else:
                    logger.warning(
                        f"Duplicate role name generated: {r['name']}. Skipping."
                    )
            return roles
        except Exception as e:
            logger.error(f"Error generating role: {str(e)}", exc_info=True)
            logger.error(f"Prompt used for role generation: {prompt}")
            return [
                Role(
                    id="default",
                    name="Task Assistant",
                    description="Assist with the given task or query.",
                    priority=5,
                    status=RoleStatus.ACTIVE,
                )
            ]

    async def generate_goals(self) -> List[Goal]:
        """
        Generate goals based on the Framer's context.

        Returns:
            List[GoalModel]: A list of generated goals.
        """
        soul = getattr(self.execution_context, "soul", {})
        prompt = f"""Generate a goal that aligns with the Framer's current context. 
        The goal should be clear, relevant, and directly related to the given information.
        Avoid creating complex scenarios. Keep it simple and focused.
        
        Soul: {json.dumps(soul, indent=2)}
        
        Respond with a JSON object containing 'name', 'description', 'priority', and 'status' fields for the goal.
        Ensure the priority is an integer between 1 and 10, where 10 is the highest priority.
        The status should be one of: 'ACTIVE', 'COMPLETED', or 'ABANDONED'.
        Consider the importance and urgency of the goal when assigning the priority and status."""

        logger.debug(f"Goal generation prompt: {prompt}")
        try:
            response = await self.llm_service.get_completion(
                prompt, model=self.default_model, max_tokens=150, temperature=0.5
            )
            logger.debug(f"Goal generation response: {response}")
            if response is None:
                logger.warning(
                    "Received None response while generating goal. Using default goal."
                )
                return [
                    Goal(
                        name="Default Goal",
                        description="Assist users based on the given input.",
                        priority=5,
                        status=GoalStatus.ACTIVE,
                    )
                ]
            goal_data = json.loads(response)
            if not goal_data:
                logger.warning(
                    "Received empty response while generating goal. Using default goal."
                )
                return [
                    Goal(
                        name="Default Goal",
                        description="Assist users based on the given input.",
                        priority=5,
                        status=GoalStatus.ACTIVE,
                    )
                ]

            if isinstance(goal_data, dict):
                goal_data = [goal_data]

            goals = []
            existing_goal_names = set()
            for g in goal_data:
                g["priority"] = max(1, min(10, int(g.get("priority", 5))))
                g["status"] = GoalStatus[g.get("status", "ACTIVE")]
                if g["name"] not in existing_goal_names:
                    goals.append(Goal(**g))
                    existing_goal_names.add(g["name"])
                    logger.info(f"Generated unique goal: {g['name']}")
                else:
                    logger.warning(
                        f"Duplicate goal name generated: {g['name']}. Skipping."
                    )
            return goals
        except Exception as e:
            logger.error(f"Error generating goal: {e}", exc_info=True)
            logger.error(f"Prompt used for goal generation: {prompt}")
            return [
                Goal(
                    name="Default Goal",
                    description="Assist users to the best of my abilities",
                    priority=5,
                    status=GoalStatus.ACTIVE,
                )
            ]

    async def generate_roles_and_goals(self) -> Tuple[List[Role], List[Goal]]:
        """
        Generate roles and goals for the Framer.

        This method generates roles and goals based on the current state:
        1. If roles are empty, generate new roles.
        2. If goals are empty, generate new goals.
        3. If both exist, generate new goals and add them to existing ones.

        Returns:
            Tuple[List[Role], List[Goal]]: A tuple containing the final roles and goals.
        """
        new_roles = await self.generate_roles()
        new_goals = await self.generate_goals()
        if self.roles is None:
            roles = new_roles
        else:
            roles = self.roles + new_roles
        if self.goals is None:
            goals = new_goals
        else:
            goals = self.goals + new_goals
        return roles, goals

    async def execute_task(self, task: Task) -> str:
        """
        Execute a task using the LLM service.

        Args:
            task (Task): The task to execute.

        Returns:
            str: The result of the task execution.
        """
        prompt = f"Execute the following task: {task.description}"
        initial_calls = self.llm_service.get_total_calls()
        initial_cost = self.llm_service.get_total_cost()

        response = await self.llm_service.get_completion(
            prompt,
            model=self.default_model,
            max_tokens=200,
            temperature=0.7,
        )

        final_calls = self.llm_service.get_total_calls()
        final_cost = self.llm_service.get_total_cost()

        task.update_status(TaskStatus.COMPLETED)
        task.set_result(response)

        calls_made = final_calls - initial_calls
        cost_incurred = final_cost - initial_cost

        logger.debug(f"Task '{task.description}' completed.")
        logger.debug(f"Calls made: {calls_made}")
        logger.debug(f"Cost incurred: ${cost_incurred:.4f}")

        return response

    def update_role_status(self, role_id: str, new_status: RoleStatus) -> None:
        for role in self.roles:
            if role.id == role_id:
                role.status = new_status
                break

    def update_goal_status(self, goal_name: str, new_status: GoalStatus) -> None:
        for goal in self.goals:
            if goal.name == goal_name:
                goal.status = new_status
                break

    async def evaluate_roles_and_goals(self) -> None:
        # Implement role and goal evaluation logic here
        pass

    def set_framer(self, framer):
        """
        Set the Framer instance associated with this Agency.

        Args:
            framer (Framer): The Framer instance to associate with this Agency.
        """
        self.framer = framer
    def add_goal(self, goal: Goal) -> None:
        """
        Add a new goal to the Agency.

        Args:
            goal (Goal): The goal to add.
        """
        self.goals.append(goal)
