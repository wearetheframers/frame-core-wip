import pytest
from frame.src.framer.agency.tasks.workflow.workflow import Workflow
from frame.src.framer.agency.tasks.task import Task
from frame.src.models.framer.agency.tasks.task import TaskStatus


@pytest.fixture
def sample_workflow():
    return Workflow("Test Workflow")


def test_workflow_initialization(sample_workflow):
    assert sample_workflow.name == "Test Workflow"
    assert sample_workflow.is_async == False
    assert len(sample_workflow.tasks) == 0
    assert sample_workflow.final_task is None


def test_add_task(sample_workflow):
    task = Task(description="Test Task", workflow_id=sample_workflow.id)
    sample_workflow.add_task(task)
    assert len(sample_workflow.tasks) == 1
    assert sample_workflow.tasks[0] == task


def test_get_task(sample_workflow):
    task = Task(description="Test Task", workflow_id=sample_workflow.id)
    sample_workflow.add_task(task)
    retrieved_task = sample_workflow.get_task(task.id)
    assert retrieved_task == task
    assert sample_workflow.get_task("non_existent_id") is None


def test_set_final_task(sample_workflow):
    final_task = Task(description="Final Task", workflow_id=sample_workflow.id)
    sample_workflow.set_final_task(final_task)
    assert sample_workflow.final_task == final_task


def test_is_complete(sample_workflow):
    task1 = Task(description="Task 1", workflow_id=sample_workflow.id)
    task2 = Task(description="Task 2", workflow_id=sample_workflow.id)
    sample_workflow.add_task(task1)
    sample_workflow.add_task(task2)

    assert sample_workflow.is_complete() == False

    task1.status = TaskStatus.COMPLETED
    assert sample_workflow.is_complete() == False

    task2.status = TaskStatus.COMPLETED
    assert sample_workflow.is_complete() == True


def test_get_next_task(sample_workflow):
    task1 = Task(description="Task 1", workflow_id=sample_workflow.id)
    task2 = Task(description="Task 2", workflow_id=sample_workflow.id)
    sample_workflow.add_task(task1)
    sample_workflow.add_task(task2)

    assert sample_workflow.get_next_task() == task1

    task1.status = TaskStatus.COMPLETED
    assert sample_workflow.get_next_task() == task2

    task2.status = TaskStatus.COMPLETED
    assert sample_workflow.get_next_task() is None
