from typing import List, Dict, Any, Optional, Tuple, Union
from frame.src.framer.agency.tasks.task import Task, TaskStatus
from frame.src.framer.agency.tasks.workflow import WorkflowManager, Workflow
from frame.src.services.llm.main import LLMService
from frame.src.services.context.context_service import Context
from frame.src.framer.agency.execution_context import ExecutionContext
from frame.src.framer.agency.action_registry import ActionRegistry
import json
import logging
import time

logger = logging.getLogger(__name__)


class Agency:
    """
    The Agency class represents the decision-making and task management component of a Framer.

    To extend the Agency's capabilities, you can add new actions to the ActionRegistry.
    This allows the Agency to perform additional tasks and manage new workflows.
    It manages roles, goals, tasks, and workflows for the Framer.

    Attributes:
        execution_context (ExecutionContext): The execution context containing necessary services.
        roles (List[Dict[str, Any]]): List of roles assigned to the Agency.
        goals (List[Dict[str, Any]]): List of goals for the Agency.
        workflow_manager (WorkflowManager): Manages workflows and tasks.
    """

    def __init__(
        self,
        llm_service: LLMService,
        context: Optional[Dict[str, Any]] = None,
        execution_context: Optional[ExecutionContext] = None,
        roles: Optional[List[Dict[str, Any]]] = None,
        goals: Optional[List[Dict[str, Any]]] = None,
    ):
        """
        Initialize an Agency instance.

        Args:
            llm_service (LLMService): The language model service.
            context (Optional[Dict[str, Any]]): Additional context for the Agency. Defaults to None.
            execution_context (Optional[ExecutionContext]): The execution context for the Agency. Defaults to None.
            roles (Optional[List[Dict[str, Any]]]): Initial roles for the Agency. Defaults to None.
            goals (Optional[List[Dict[str, Any]]]): Initial goals for the Agency. Defaults to None.
        """
        self.llm_service = llm_service
        self.context = context or {}
        self.execution_context = execution_context or ExecutionContext(
            llm_service=llm_service
        )
        self.roles = roles if roles is not None else []
        self.goals = goals if goals is not None else []
        self.workflow_manager = WorkflowManager()
        self.completion_calls = {}
        self.default_model = getattr(self.llm_service, "default_model", "gpt-3.5-turbo")
        self.action_registry = ActionRegistry(self.execution_context)

    def add_role(self, role: Dict[str, Any]) -> None:
        """
        Add a new role to the Agency.

        Args:
            role (Dict[str, Any]): The role to be added.
        """
        self.roles.append(role)

    def set_roles(self, roles: Optional[List[Dict[str, Any]]] = None) -> None:
        """
        Set the roles for the Agency.

        Args:
            roles (Optional[List[Dict[str, Any]]]): List of role dictionaries.
        """
        self.roles = roles if roles is not None else []

    def set_goals(self, goals: Optional[List[Dict[str, Any]]] = None):
        """
        Set the goals for the Agency.

        Args:
            goals (Optional[List[Dict[str, Any]]]): List of goal dictionaries.
        """
        self.goals = goals if goals is not None else []

    def add_goal(self, goal: Dict[str, Any]) -> None:
        """
        Add a new goal to the Agency.

        Args:
            goal (Dict[str, Any]): The goal to be added.
        """
        self.goals.append(goal)

    def get_roles(self) -> List[Dict[str, Any]]:
        """
        Get all roles of the Agency.

        Returns:
            List[Dict[str, Any]]: List of all roles.
        """
        return self.roles

    def get_goals(self) -> List[Dict[str, Any]]:
        """
        Get all goals of the Agency.

        Returns:
            List[Dict[str, Any]]: List of all goals.
        """
        return self.goals

    def create_task(
        self,
        description: str,
        priority: Union[float, str] = 50.0,
        workflow_id: str = "default",
    ) -> Task:
        """
        Create a new task with the given description and priority.

        Args:
            description (str): The description of the task.
            priority (Union[float, str], optional): The priority of the task. Can be a float or a string. Defaults to 50.0.
            workflow_id (str, optional): The ID of the workflow this task belongs to. Defaults to "default".

        Returns:
            Task: The created Task object.
        """
        if isinstance(priority, str):
            priority_map = {"Low": 25.0, "Medium": 50.0, "High": 75.0}
            priority = priority_map.get(priority.capitalize(), 50.0)
        return Task(
            description=description, priority=float(priority), workflow_id=workflow_id
        )

    def add_task(self, task: Task, workflow_id: str = "default") -> None:
        """
        Add a new task to a specified workflow.

        Args:
            task (Task): The task to add.
            workflow_id (str, optional): The ID of the workflow to add the task to. Defaults to "default".
        """
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
        return max(pending_tasks, key=lambda x: x.priority) if pending_tasks else None

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

    async def generate_roles(self) -> List[Dict[str, Any]]:
        """
        Generate roles based on the Framer's context.

        Returns:
            List[Dict[str, Any]]: A list of generated roles.
        """
        soul = getattr(self.context, "soul", {})
        prompt = f"""Generate a role that aligns with the Framer's current context. 
        The role should be clear, relevant, and directly related to the given information.
        Avoid creating complex scenarios. Keep it simple and focused.
        
        Soul: {json.dumps(soul, indent=2)}
        
        Respond with a JSON object containing 'name' and 'description' fields for the role."""
        logger.debug(f"Role generation prompt: {prompt}")
        try:
            response = await self.llm_service.get_completion(
                prompt, model=self.default_model, max_tokens=150, temperature=0.5
            )
            logger.debug(f"Role generation response: {response}")
            role = json.loads(response)
            if not role:
                logger.warning(
                    "Received empty response while generating role. Using default role."
                )
                return [
                    {
                        "name": "Task Assistant",
                        "description": "Assist with the given task or query.",
                    }
                ]
            return [role] if isinstance(role, dict) else role
        except Exception as e:
            logger.error(f"Error generating role: {str(e)}", exc_info=True)
            logger.error(f"Prompt used for role generation: {prompt}")
            return [
                {
                    "name": "Task Assistant",
                    "description": "Assist with the given task or query.",
                }
            ]

    async def generate_goals(self) -> List[Dict[str, Any]]:
        """
        Generate goals based on the Framer's context.

        Returns:
            List[Dict[str, Any]]: A list of generated goals.
        """
        soul = getattr(self.context, "soul", {})
        prompt = f"""Generate a goal that aligns with the Framer's current context. 
        The goal should be clear, relevant, and directly related to the given information.
        Avoid creating complex scenarios. Keep it simple and focused.
        
        Soul: {json.dumps(soul, indent=2)}
        
        Respond with a JSON object containing 'description' and 'priority' fields for the goal."""

        logger.debug(f"Goal generation prompt: {prompt}")
        try:
            response = await self.llm_service.get_completion(
                prompt, model=self.default_model, max_tokens=150, temperature=0.5
            )
            logger.debug(f"Goal generation response: {response}")
            goal = json.loads(response)
            if not goal:
                logger.warning(
                    "Received empty response while generating goal. Using default goal."
                )
                return [
                    {
                        "description": "Assist users based on the given input.",
                        "priority": 50.0,
                    }
                ]
            return [goal] if isinstance(goal, dict) else goal
        except Exception as e:
            logger.error(f"Error generating goal: {e}", exc_info=True)
            logger.error(f"Prompt used for goal generation: {prompt}")
            return [
                {
                    "description": "Assist users to the best of my abilities",
                    "priority": 1,
                }
            ]

    async def generate_goals(self) -> List[Dict[str, Any]]:
        """
        Generate goals based on the Framer's context.

        Returns:
            List[Dict[str, Any]]: A list of generated goals.
        """
        soul = getattr(self.context, "soul", {})
        prompt = f"""Generate a goal that aligns with the Framer's current context. 
        The goal should be clear, relevant, and directly related to the given information.
        Avoid creating complex scenarios. Keep it simple and focused.
        
        Soul: {json.dumps(soul, indent=2)}
        
        Respond with a JSON object containing 'description' and 'priority' fields for the goal."""

        logger.debug(f"Goal generation prompt: {prompt}")
        try:
            response = await self.llm_service.get_completion(
                prompt, model=self.default_model, max_tokens=150, temperature=0.5
            )
            logger.debug(f"Goal generation response: {response}")
            goal = json.loads(response)
            if not goal:
                logger.warning(
                    "Received empty response while generating goal. Using default goal."
                )
                return [
                    {
                        "description": "Assist users based on the given input.",
                        "priority": 50.0,
                    }
                ]
            return [goal] if isinstance(goal, dict) else goal
        except Exception as e:
            logger.error(f"Error generating goal: {e}", exc_info=True)
            logger.error(f"Prompt used for goal generation: {prompt}")
            return [
                {
                    "description": "Assist users to the best of my abilities",
                    "priority": 1,
                }
            ]

    async def generate_roles_and_goals(
        self,
    ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Generate roles and goals for the Framer.

        This method generates roles and goals based on the current state:
        1. If roles are empty, generate new roles.
        2. If goals are empty, generate new goals.
        3. If both exist, generate new goals and add them to existing ones.

        Returns:
            Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]: A tuple containing
            the final roles and goals.
        """
        roles = await self.generate_roles()
        goals = await self.generate_goals()
        return roles, goals

    async def generate_roles_and_goals(
        self,
    ) -> Tuple[List[str], List[str]]:
        """
        Generate roles and goals for the Framer.

        This method generates roles and goals based on the current state:
        1. If roles are empty, generate new roles.
        2. If goals are empty, generate new goals.
        3. If both exist, generate new goals and add them to existing ones.

        Returns:
            Tuple[List[str], List[str]]: A tuple containing
            the final roles and goals as strings.
        """
        new_roles = await self.generate_roles()
        new_goals = await self.generate_goals()

        if not new_roles:
            new_roles = ["Task Assistant"]

        if not new_goals:
            new_goals = ["Assist users to the best of my abilities"]

        return new_roles, new_goals

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
