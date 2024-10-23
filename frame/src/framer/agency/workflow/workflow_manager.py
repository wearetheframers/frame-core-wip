from typing import Dict, List, Optional
from frame.src.framer.agency.tasks.task import Task
from frame.src.framer.agency.tasks.status import TaskStatus
from frame.src.framer.agency.workflow.workflow import Workflow


class WorkflowManager:
    def __init__(self):
        self.workflows: Dict[str, Workflow] = {}

    def create_workflow(self, name: str, is_async: bool = False) -> Workflow:
        workflow = Workflow(name, is_async)
        self.workflows[name] = workflow
        return workflow

    def get_workflow(self, name: str) -> Optional[Workflow]:
        return self.workflows.get(name)

    def add_task(self, workflow_name: str, task: Task):
        workflow = self.get_workflow(workflow_name)
        if workflow:
            workflow.add_task(task)
        else:
            raise ValueError(f"Workflow '{workflow_name}' not found")

    def set_final_task_for_workflow(self, workflow_name: str, task: Task):
        workflow = self.get_workflow(workflow_name)
        if workflow:
            workflow.final_task = task
        else:
            raise ValueError(f"Workflow '{workflow_name}' not found")

    def get_all_tasks(self) -> List[Task]:
        all_tasks = []
        for workflow in self.workflows.values():
            all_tasks.extend(workflow.tasks)
        return all_tasks

    def cancel_task(self, task_id: str) -> None:
        for workflow in self.workflows.values():
            for task in workflow.tasks:
                if task.id == task_id:
                    task.update_status(TaskStatus.CANCELED)
                    return
        raise ValueError(f"Task with id '{task_id}' not found in any workflow.")
        return f"WorkflowManager(workflows={len(self.workflows)})"
