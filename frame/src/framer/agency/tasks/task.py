from datetime import datetime
from typing import Any, Dict, Optional, List, Callable
from frame.src.utils.id_generator import generate_id
import logging
from frame.src.framer.agency.roles import Role
from pydantic import BaseModel, Field
from enum import Enum
from frame.src.models.framer.agency.tasks import TaskModel, TaskStatus
from frame.src.utils.id_generator import generate_id


class TaskModel(BaseModel):
    id: str
    description: str
    priority: int
    workflow_id: str
    status: TaskStatus = TaskStatus.PENDING
    expected_results: List[Any] = Field(default_factory=list)
    dependencies: List[str] = Field(default_factory=list)
    parent_task_id: Optional[str] = None
    assigned_to: Optional[str] = None
    estimated_duration: Optional[float] = None
    tags: List[str] = Field(default_factory=list)
    type: Optional[str] = None
    data: Dict[str, Any] = Field(default_factory=dict)
    result: Optional[Any] = None
    updated_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


logger = logging.getLogger(__name__)


class Task(TaskModel):
    """
    Represents a task within the Frame-Core system.

    A Task is an actionable item that Framers work on. It includes a description
    of the action to be performed, a priority level, a status, and can store
    results and metadata.
    """

    workflow_metrics: Dict[str, Dict[str, Any]] = {}
    cancel_callback: Optional[Callable[[], None]] = None

    def __init__(
        self,
        description: str,
        workflow_id: str,
        priority: int = 5,
        status: TaskStatus = TaskStatus.PENDING,
        expected_results: Optional[List[Any]] = None,
        dependencies: List[str] = None,
        parent_task_id: Optional[str] = None,
        assigned_to: Optional[str] = None,
        estimated_duration: Optional[float] = None,
        tags: List[str] = None,
        type: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None,
        updated_at: Optional[datetime] = None,
        completed_at: Optional[datetime] = None,
        stakeholders: Optional[List[Dict[str, Any]]] = None,
    ):
        self.stakeholders = stakeholders or []
        for stakeholder in self.stakeholders:
            stakeholder['id'] = stakeholder.get('id', generate_id())
            stakeholder['roles'] = stakeholder.get('roles', [])
        task_id = generate_id()
        if not (1 <= priority <= 10):
            raise ValueError("Priority must be between 1 and 10")
        super().__init__(
            id=task_id,
            description=description,
            priority=priority,
            workflow_id=workflow_id,
            expected_results=expected_results or [],
            dependencies=dependencies or [],
            parent_task_id=parent_task_id,
            assigned_to=assigned_to,
            estimated_duration=estimated_duration,
            tags=tags or [],
            type=type,
            data=data or {},
            updated_at=updated_at,
            completed_at=completed_at,
        )
        self.subtasks: List[Task] = []
        self.result = None
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.actual_duration: Optional[float] = None
        self.completed_at = completed_at
        logger.debug(
            f"Created new task with ID: {self.id} and expected results: {self.expected_results}"
        )
        self._execute_callback: Optional[Callable[[], Any]] = None

    def update_status(self, new_status: TaskStatus) -> None:
        """
        Update the status of the task.

        Args:
            new_status (TaskStatus): The new status to set for the task.
        """
        self.status = new_status
        self.updated_at = datetime.now()
        if new_status == TaskStatus.COMPLETED:
            self.completed_at = datetime.now()

    def set_result(self, result: Any) -> None:
        """
        Set the result of the task execution.

        Args:
            result (Any): The result of the task execution.
        """
        self.result = result
        self.updated_at = datetime.now()

    def add_subtask(self, subtask: "Task") -> None:
        """
        Add a subtask to this task.

        Args:
            subtask (Task): The subtask to add.
        """
        self.subtasks.append(subtask)
        subtask.parent_task_id = self.id

    def set_actual_duration(self, duration: float) -> None:
        """
        Set the actual duration of the task execution.

        Args:
            duration (float): The actual duration of the task execution.
        """
        self.actual_duration = duration
        self.updated_at = datetime.now()

    def set_execute_callback(self, callback: Callable[[], Any]) -> None:
        """
        Set the execute callback for the task.

        Args:
            callback (Callable[[], Any]): The callback function to be called when the task is executed.
        """
        self._execute_callback = callback

    def set_cancel_callback(self, callback: Callable[[], None]) -> None:
        """
        Set the cancel callback for the task.

        Args:
            callback (Callable[[], None]): The callback function to be called when the task is cancelled.
        """
        self.cancel_callback = callback

    async def execute(self) -> Any:
        """
        Execute the task.

        Returns:
            Any: The result of the task execution.
        """
        if self._execute_callback:
            self.result = await self._execute_callback()
            self.status = TaskStatus.COMPLETED
            return self.result
        else:
            raise NotImplementedError("Task execution not implemented")

    def cancel(self) -> None:
        """
        Cancel the task.
        """
        if self.cancel_callback:
            self.cancel_callback()
        self.status = TaskStatus.CANCELED

    def log_workflow_metrics(self, workflow_id: str) -> None:
        """
        Log and save the completion call metrics for a completed workflow.

        Args:
            workflow_id (str): The ID of the completed workflow.
        """
        # Placeholder data
        metrics = {"total_tasks": 5, "completed_tasks": 3, "total_time": 10.5}
        logger.info(f"Workflow {workflow_id} completed.")
        logger.info(f"Workflow metrics: {metrics}")

        # Save metrics
        self.workflow_metrics[workflow_id] = metrics

        for task_id, task_metric in metrics.get("tasks", {}).items():
            logger.info(f"  Task {task_id}: {task_metric}")

    def get_workflow(self, workflow_id: str):
        """
        Placeholder method to get a workflow. In a real implementation, this would
        retrieve the workflow from some storage or management system.
        """
        return None

    def get_workflow_metrics(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve the metrics for a completed workflow.

        Args:
            workflow_id (str): The ID of the completed workflow.

        Returns:
            Optional[Dict[str, Any]]: The metrics for the workflow, or None if not found.
        """
        return self.workflow_metrics.get(workflow_id)

    def get_all_workflow_metrics(self) -> Dict[str, Dict[str, Any]]:
        """
        Retrieve metrics for all completed workflows.

        Returns:
            Dict[str, Dict[str, Any]]: A dictionary of all workflow metrics.
        """
        return self.workflow_metrics

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the Task object to a dictionary representation.

        Returns:
            Dict[str, Any]: A dictionary representation of the Task.
        """
        return {
            "id": self.id,
            "description": self.description,
            "workflow_id": self.workflow_id,
            "priority": self.priority,
            "status": self.status.value,
            "result": self.result,
            "expected_results": self.expected_results,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "completed_at": (
                self.completed_at.isoformat() if self.completed_at else None
            ),
            "metadata": self.metadata,
            "dependencies": self.dependencies,
            "subtasks": [subtask.to_dict() for subtask in self.subtasks],
            "parent_task_id": self.parent_task_id,
            "assigned_to": self.assigned_to,
            "estimated_duration": self.estimated_duration,
            "actual_duration": self.actual_duration,
            "tags": self.tags,
        }
