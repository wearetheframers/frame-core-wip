from typing import Dict, Optional
from frame.src.framer.agency.tasks.workflow.workflow import Workflow
from frame.src.framer.agency.tasks.task import Task, TaskStatus

from typing import List, Dict, Callable


class WorkflowManager:
    """
    Manages workflows within the Framer system.
    """

    def __init__(self):
        self.workflows: Dict[str, Workflow] = {}
        self._cancel_callbacks: List[Callable[[], None]] = []

    def create_workflow(self, name: str, is_async: bool = False) -> Workflow:
        """
        Create a new workflow.

        Args:
            name (str): The name of the new workflow.
            is_async (bool, optional): Whether the workflow is asynchronous. Defaults to False.

        Returns:
            Workflow: The newly created workflow.
        """
        workflow = Workflow(name, is_async)
        self.workflows[name] = workflow
        return workflow

    def get_workflow(self, workflow_id: str) -> Optional[Workflow]:
        """
        Get a workflow by its ID.

        Args:
            workflow_id (str): The ID of the workflow to retrieve.

        Returns:
            Optional[Workflow]: The workflow if found, None otherwise.
        """
        return self.workflows.get(workflow_id)

    def add_task(self, workflow_id: str, task: Task) -> None:
        """
        Add a new task to a specified workflow.

        Args:
            workflow_id (str): The ID of the workflow to add the task to.
            task (Task): The task to add to the workflow.
        """
        if workflow_id not in self.workflows:
            self.workflows[workflow_id] = Workflow(workflow_id)
        self.workflows[workflow_id].add_task(task)

    def set_final_task_for_workflow(self, workflow_name: str, task: Task) -> None:
        """
        Set the final task for a specified workflow.

        Args:
            workflow_name (str): The name of the workflow.
            task (Task): The task to set as the final task.
        """
        if workflow_name in self.workflows:
            self.workflows[workflow_name].set_final_task(task)

    async def cancel_workflow(self):
        """
        Cancel the currently executing workflow.
        """
        for callback in self._cancel_callbacks:
            callback()
        self._cancel_callbacks.clear()

    async def cancel_task(self, task_id: str):
        """
        Cancel a specific task.

        Args:
            task_id (str): The ID of the task to cancel.
        """
        for workflow in self.workflows.values():
            task = workflow.get_task(task_id)
            if task:
                task.status = TaskStatus.CANCELED
                if task.cancel_callback:
                    task.cancel_callback()
                return
        raise ValueError(f"Task with ID {task_id} not found")
