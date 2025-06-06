import asyncio
from typing import List, Optional, Dict, Any
from frame.src.framer.agency.roles import Role
from frame.src.utils.id_generator import generate_id
from frame.src.framer.agency.tasks.task import Task


class Workflow:
    def __init__(
        self,
        name: str,
        is_async: bool = False,
        stakeholders: Optional[List[Dict[str, Any]]] = None,
    ):
        self.id = generate_id()
        self.stakeholders = stakeholders or []
        for stakeholder in self.stakeholders:
            stakeholder["id"] = stakeholder.get("id", generate_id())
            stakeholder["roles"] = stakeholder.get("roles", [])
        self.name = name
        self.tasks: List[Task] = []
        self.is_async = is_async
        self.final_task: Optional[Task] = None

    def add_task(self, task: Task):
        self.tasks.append(task)

    def set_final_task(self, task: Task):
        self.final_task = task

    def get_tasks(self) -> List[Task]:
        return self.tasks

    def cancel_task(self, task_id: str) -> None:
        """
        Cancel a task by its ID.

        Args:
            task_id (str): The ID of the task to cancel.
        """
        # Implementation of cancellation logic
        print(f"Task {task_id} has been cancelled.")

    def __str__(self):
        return f"Workflow(name={self.name}, tasks={len(self.tasks)}, is_async={self.is_async})"
