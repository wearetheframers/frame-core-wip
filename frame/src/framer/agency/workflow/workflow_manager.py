from typing import Dict, List, Optional
from frame.src.framer.agency.tasks.task import Task
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
            workflow.set_final_task(task)
        else:
            raise ValueError(f"Workflow '{workflow_name}' not found")

    def get_all_tasks(self) -> List[Task]:
        all_tasks = []
        for workflow in self.workflows.values():
            all_tasks.extend(workflow.get_tasks())
        return all_tasks

    def __str__(self):
        return f"WorkflowManager(workflows={len(self.workflows)})"
