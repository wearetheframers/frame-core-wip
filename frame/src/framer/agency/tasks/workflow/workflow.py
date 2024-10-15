from typing import Optional, List
from frame.src.utils.id_generator import generate_id
from frame.src.framer.agency.tasks.task import Task
from frame.src.models.framer.agency.tasks.task import TaskStatus


class Workflow:
    """
    Represents a workflow within the Frame-Core system.

    A Workflow is a sequence of related tasks that need to be completed to achieve a specific goal.
    It manages the execution and state of its tasks, and provides methods for adding, retrieving,
    and completing tasks.

    Attributes:
        id (str): The unique identifier for the workflow.
        name (str): The name of the workflow.
        is_async (bool): Whether the workflow is asynchronous.
        tasks (List[Task]): The list of tasks in the workflow.
        final_task (Optional[Task]): The final task of the workflow.
    """

    def __init__(self, name: str, is_async: bool = False):
        self.id = generate_id()
        self.name = name
        self.is_async = is_async
        self.tasks: List[Task] = []
        self.final_task: Optional[Task] = None

    def add_task(self, task: Task) -> None:
        """
        Add a task to the workflow.

        Args:
            task (Task): The task to add to the workflow.
        """
        self.tasks.append(task)

    def get_task(self, task_id: str) -> Optional[Task]:
        """
        Get a task by its ID.

        Args:
            task_id (str): The ID of the task to retrieve.

        Returns:
            Optional[Task]: The task if found, None otherwise.
        """
        return next((task for task in self.tasks if task.id == task_id), None)

    def set_final_task(self, task: Task) -> None:
        """
        Set the final task for the workflow.

        Args:
            task (Task): The task to set as the final task.
        """
        self.final_task = task

    def is_complete(self) -> bool:
        """
        Check if the workflow is complete.

        Returns:
            bool: True if all tasks are completed, False otherwise.
        """
        return all(task.status == TaskStatus.COMPLETED for task in self.tasks)

    def get_next_task(self) -> Optional[Task]:
        """
        Get the next task to be executed in the workflow.

        Returns:
            Optional[Task]: The next task to be executed, or None if all tasks are completed.
        """
        for task in self.tasks:
            if task.status == TaskStatus.PENDING:
                return task
        return None

    def get_task(self, task_id: str) -> Optional[Task]:
        """
        Get a task by its ID.

        Args:
            task_id (str): The ID of the task to retrieve.

        Returns:
            Optional[Task]: The task if found, None otherwise.
        """
        return next((task for task in self.tasks if task.id == task_id), None)
