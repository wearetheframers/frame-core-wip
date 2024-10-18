from typing import Any, Optional
from frame.src.services.execution_context import ExecutionContext
from frame.src.framer.agency.priority import Priority
from frame.src.framer.agency.tasks.task import Task


class BaseAction:
    """
    Base class for all actions in the Frame framework.
    Actions can create Tasks, which can enforce output types.
    """

    def __init__(
        self, name: str, description: str, priority: Priority = Priority.MEDIUM
    ):
        self.name = name
        self.description = description
        self.priority = priority

    async def execute(self, execution_context: ExecutionContext, **kwargs: Any) -> Any:
        """
        Execute the action.

        Args:
            execution_context (ExecutionContext): The execution context containing necessary services.
            **kwargs: Additional keyword arguments that might be passed to the action.

        Returns:
            Any: The result of the action execution, which could be a Task or any other type.
        """
        raise NotImplementedError("Subclasses must implement this method")

    def create_task(
        self, description: str, expected_output_type: Optional[type] = None, **kwargs
    ) -> Task:
        """
        Create a new Task with the given description and expected output type.

        Args:
            description (str): The description of the task.
            expected_output_type (Optional[type]): The expected output type of the task.
            **kwargs: Additional keyword arguments for Task creation.

        Returns:
            Task: A new Task instance.
        """
        return Task(
            description=description, expected_output_type=expected_output_type, **kwargs
        )

    def __str__(self):
        return f"BaseAction(name={self.name}, priority={self.priority})"
