import pytest
from datetime import datetime
from frame.src.framer.agency.tasks.task import Task
from frame.src.models.framer.agency.tasks.task import TaskStatus
import json
from unittest.mock import patch


@pytest.fixture
def sample_task():
    task = Task(
        description="Test task",
        workflow_id="test_workflow",
        priority=5,
        expected_results=["Result 1", "Result 2"],
        dependencies=["task1", "task2"],
        parent_task_id="parent_task",
        assigned_to="test_user",
        estimated_duration=3.5,
        tags=["test", "sample"],
    )
    task.llm_service.get_completion.return_value = json.dumps({
        "name": "Role1",
        "description": "A test role",
        "priority": 5,
    })
    return task


def test_task_initialization(sample_task):
    assert sample_task.description == "Test task"
    assert sample_task.workflow_id == "test_workflow"
    assert sample_task.priority == 5
    assert sample_task.expected_results == ["Result 1", "Result 2"]
    assert sample_task.dependencies == ["task1", "task2"]
    assert sample_task.parent_task_id == "parent_task"
    assert sample_task.assigned_to == "test_user"
    assert sample_task.estimated_duration == 3.5
    assert sample_task.tags == ["test", "sample"]
    assert sample_task.status == TaskStatus.PENDING
    assert isinstance(sample_task.created_at, datetime)
    assert isinstance(sample_task.updated_at, datetime)
    assert sample_task.completed_at is None


def test_update_status(sample_task):
    sample_task.update_status(TaskStatus.IN_PROGRESS)
    assert sample_task.status == TaskStatus.IN_PROGRESS
    assert sample_task.completed_at is None

    sample_task.update_status(TaskStatus.COMPLETED)
    assert sample_task.status == TaskStatus.COMPLETED
    assert isinstance(sample_task.completed_at, datetime)


def test_set_result(sample_task):
    result = "Task completed successfully"
    sample_task.set_result(result)
    assert sample_task.result == result


def test_add_subtask(sample_task):
    subtask = Task(description="Subtask", workflow_id="test_workflow")
    sample_task.add_subtask(subtask)
    assert subtask in sample_task.subtasks
    assert subtask.parent_task_id == sample_task.id


def test_set_actual_duration(sample_task):
    duration = 4.5
    sample_task.set_actual_duration(duration)
    assert sample_task.actual_duration == duration


def test_to_dict(sample_task):
    task_dict = sample_task.to_dict()
    assert isinstance(task_dict, dict)
    assert task_dict["description"] == "Test task"
    assert task_dict["workflow_id"] == "test_workflow"
    assert task_dict["priority"] == 5
    assert task_dict["expected_results"] == ["Result 1", "Result 2"]
    assert task_dict["dependencies"] == ["task1", "task2"]
    assert task_dict["parent_task_id"] == "parent_task"
    assert task_dict["assigned_to"] == "test_user"
    assert task_dict["estimated_duration"] == 3.5
    assert task_dict["tags"] == ["test", "sample"]
    assert task_dict["status"] == TaskStatus.PENDING.value


def test_workflow_metrics(sample_task):
    workflow_id = "test_workflow"
    sample_task.log_workflow_metrics(workflow_id)
    assert sample_task.get_workflow_metrics(workflow_id) == {
        "total_tasks": 5,
        "completed_tasks": 3,
        "total_time": 10.5,
    }
    assert workflow_id in sample_task.get_all_workflow_metrics()


import pytest
from datetime import datetime
from frame.src.framer.agency.tasks.task import Task
from frame.src.models.framer.agency.tasks.task import TaskStatus
from unittest.mock import patch


@pytest.fixture
def sample_task():
    return Task(
        description="Test task",
        workflow_id="test_workflow",
        priority=50,
        expected_results=["Result 1", "Result 2"],
        dependencies=["task1", "task2"],
        parent_task_id="parent_task",
        assigned_to="test_user",
        estimated_duration=3.5,
        tags=["test", "sample"],
    )


def test_task_initialization(sample_task):
    assert sample_task.description == "Test task"
    assert sample_task.workflow_id == "test_workflow"
    assert sample_task.priority == 50
    assert sample_task.expected_results == ["Result 1", "Result 2"]
    assert sample_task.dependencies == ["task1", "task2"]
    assert sample_task.parent_task_id == "parent_task"
    assert sample_task.assigned_to == "test_user"
    assert sample_task.estimated_duration == 3.5
    assert sample_task.tags == ["test", "sample"]
    assert sample_task.status == TaskStatus.PENDING
    assert isinstance(sample_task.created_at, datetime)
    assert isinstance(sample_task.updated_at, datetime)
    assert sample_task.completed_at is None


def test_update_status(sample_task):
    sample_task.update_status(TaskStatus.IN_PROGRESS)
    assert sample_task.status == TaskStatus.IN_PROGRESS
    assert sample_task.completed_at is None

    sample_task.update_status(TaskStatus.COMPLETED)
    assert sample_task.status == TaskStatus.COMPLETED
    assert isinstance(sample_task.completed_at, datetime)


def test_set_result(sample_task):
    result = "Task completed successfully"
    sample_task.set_result(result)
    assert sample_task.result == result


def test_add_subtask(sample_task):
    subtask = Task(description="Subtask", workflow_id="test_workflow")
    sample_task.add_subtask(subtask)
    assert subtask in sample_task.subtasks
    assert subtask.parent_task_id == sample_task.id


def test_set_actual_duration(sample_task):
    duration = 4.5
    sample_task.set_actual_duration(duration)
    assert sample_task.actual_duration == duration


def test_to_dict(sample_task):
    task_dict = sample_task.to_dict()
    assert isinstance(task_dict, dict)
    assert task_dict["description"] == "Test task"
    assert task_dict["workflow_id"] == "test_workflow"
    assert task_dict["priority"] == 50
    assert task_dict["expected_results"] == ["Result 1", "Result 2"]
    assert task_dict["dependencies"] == ["task1", "task2"]
    assert task_dict["parent_task_id"] == "parent_task"
    assert task_dict["assigned_to"] == "test_user"
    assert task_dict["estimated_duration"] == 3.5
    assert task_dict["tags"] == ["test", "sample"]
    assert task_dict["status"] == TaskStatus.PENDING.value


def test_workflow_metrics(sample_task):
    workflow_id = "test_workflow"
    sample_task.log_workflow_metrics(workflow_id)
    assert sample_task.get_workflow_metrics(workflow_id) == {
        "total_tasks": 5,
        "completed_tasks": 3,
        "total_time": 10.5,
    }
    assert workflow_id in sample_task.get_all_workflow_metrics()
