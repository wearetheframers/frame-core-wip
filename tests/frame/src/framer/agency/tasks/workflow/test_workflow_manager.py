import pytest
from frame.src.framer.agency.tasks.workflow.workflow_manager import WorkflowManager
from frame.src.framer.agency.tasks.task import Task


@pytest.fixture
def workflow_manager():
    return WorkflowManager()


def test_create_workflow(workflow_manager):
    workflow = workflow_manager.create_workflow("Test Workflow")
    assert workflow.name == "Test Workflow"
    assert workflow.is_async == False
    assert workflow_manager.get_workflow("Test Workflow") == workflow


def test_create_async_workflow(workflow_manager):
    workflow = workflow_manager.create_workflow("Async Workflow", is_async=True)
    assert workflow.name == "Async Workflow"
    assert workflow.is_async == True


def test_get_workflow(workflow_manager):
    workflow_manager.create_workflow("Test Workflow")
    retrieved_workflow = workflow_manager.get_workflow("Test Workflow")
    assert retrieved_workflow.name == "Test Workflow"
    assert workflow_manager.get_workflow("Non-existent Workflow") is None


def test_add_task(workflow_manager):
    workflow_manager.create_workflow("Test Workflow")
    task = Task(description="Test Task", workflow_id="Test Workflow")
    workflow_manager.add_task("Test Workflow", task)
    workflow = workflow_manager.get_workflow("Test Workflow")
    assert len(workflow.tasks) == 1
    assert workflow.tasks[0] == task


def test_add_task_to_non_existent_workflow(workflow_manager):
    task = Task(description="Test Task", workflow_id="Non-existent Workflow")
    workflow_manager.add_task("Non-existent Workflow", task)
    workflow = workflow_manager.get_workflow("Non-existent Workflow")
    assert workflow is not None
    assert len(workflow.tasks) == 1
    assert workflow.tasks[0] == task


def test_set_final_task_for_workflow(workflow_manager):
    workflow_manager.create_workflow("Test Workflow")
    final_task = Task(description="Final Task", workflow_id="Test Workflow")
    workflow_manager.set_final_task_for_workflow("Test Workflow", final_task)
    workflow = workflow_manager.get_workflow("Test Workflow")
    assert workflow.final_task == final_task


def test_set_final_task_for_non_existent_workflow(workflow_manager):
    final_task = Task(description="Final Task", workflow_id="Non-existent Workflow")
    workflow_manager.set_final_task_for_workflow("Non-existent Workflow", final_task)
    # This should not raise an error, but the final task won't be set
    assert "Non-existent Workflow" not in workflow_manager.workflows


import pytest
from frame.src.framer.agency.tasks.workflow.workflow_manager import WorkflowManager
from frame.src.framer.agency.tasks.task import Task


@pytest.fixture
def workflow_manager():
    return WorkflowManager()


def test_create_workflow(workflow_manager):
    workflow = workflow_manager.create_workflow("Test Workflow")
    assert workflow.name == "Test Workflow"
    assert workflow.is_async == False
    assert workflow_manager.get_workflow("Test Workflow") == workflow


def test_create_async_workflow(workflow_manager):
    workflow = workflow_manager.create_workflow("Async Workflow", is_async=True)
    assert workflow.name == "Async Workflow"
    assert workflow.is_async == True


def test_get_workflow(workflow_manager):
    workflow_manager.create_workflow("Test Workflow")
    retrieved_workflow = workflow_manager.get_workflow("Test Workflow")
    assert retrieved_workflow.name == "Test Workflow"
    assert workflow_manager.get_workflow("Non-existent Workflow") is None


def test_add_task(workflow_manager):
    workflow_manager.create_workflow("Test Workflow")
    task = Task(description="Test Task", workflow_id="Test Workflow")
    workflow_manager.add_task("Test Workflow", task)
    workflow = workflow_manager.get_workflow("Test Workflow")
    assert len(workflow.tasks) == 1
    assert workflow.tasks[0] == task


def test_add_task_to_non_existent_workflow(workflow_manager):
    task = Task(description="Test Task", workflow_id="Non-existent Workflow")
    workflow_manager.add_task("Non-existent Workflow", task)
    workflow = workflow_manager.get_workflow("Non-existent Workflow")
    assert workflow is not None
    assert len(workflow.tasks) == 1
    assert workflow.tasks[0] == task


def test_set_final_task_for_workflow(workflow_manager):
    workflow_manager.create_workflow("Test Workflow")
    final_task = Task(description="Final Task", workflow_id="Test Workflow")
    workflow_manager.set_final_task_for_workflow("Test Workflow", final_task)
    workflow = workflow_manager.get_workflow("Test Workflow")
    assert workflow.final_task == final_task


def test_set_final_task_for_non_existent_workflow(workflow_manager):
    final_task = Task(description="Final Task", workflow_id="Non-existent Workflow")
    workflow_manager.set_final_task_for_workflow("Non-existent Workflow", final_task)
    # This should not raise an error, but the final task won't be set
    assert "Non-existent Workflow" not in workflow_manager.workflows
