import pytest
from frame.src.framer.brain.decision import Decision
from frame.src.framer.agency.action_registry import ActionRegistry
from frame.src.framer.agency.tasks import TaskStatusModel
from frame.src.framer.agency.execution_context import ExecutionContext


def test_decision_initialization():
    decision = Decision(
        action="respond",
        parameters={"response": "Hello, world!"},
        reasoning="Greeting the user",
        confidence=0.9,
        priority=5,
        task_status=TaskStatusModel.IN_PROGRESS,
    )

    assert decision.action == "respond"
    assert decision.parameters == {"response": "Hello, world!"}
    assert decision.reasoning == "Greeting the user"
    assert decision.confidence == 0.9
    assert decision.priority == 5
    assert decision.expected_results == []  # Default value is an empty list
    assert decision.task_status == TaskStatusModel.IN_PROGRESS


def test_decision_from_json():
    json_str = '{"action": "research", "parameters": {"topic": "AI"}, "reasoning": "Gather information", "confidence": 0.8, "priority": 7, "task_status": "in_progress"}'
    decision = Decision.parse_raw(json_str)

    assert decision.action == "research"
    assert decision.parameters == {"topic": "AI"}
    assert decision.reasoning == "Gather information"
    assert decision.confidence == 0.8
    assert decision.priority == 7
    assert decision.task_status == TaskStatusModel.IN_PROGRESS
    assert decision.expected_results == []  # Default is an empty list


def test_decision_to_dict():
    decision = Decision(
        action="generate_tasks",
        parameters={"tasks": ["Task 1", "Task 2"]},
        reasoning="Creating new tasks",
        confidence=0.7,
        priority=6,
        expected_results=["Completed Task 1", "Completed Task 2"],
        task_status=TaskStatusModel.COMPLETED,
    )

    decision_dict = decision.to_dict()

    assert decision_dict["action"] == "generate_tasks"
    assert decision.parameters == {"tasks": ["Task 1", "Task 2"]}
    assert decision_dict["reasoning"] == "Creating new tasks"
    assert decision.confidence == 0.7
    assert decision.priority == 6
    assert decision.task_status == TaskStatusModel.COMPLETED
    assert decision.expected_results == ["Completed Task 1", "Completed Task 2"]


def test_decision_create():
    decision = Decision(
        action="wait",
        parameters={},
        reasoning="No action needed",
        confidence=0.5,
        priority=1,
        expected_results=[],  # Explicitly set an empty list
        task_status=TaskStatusModel.PENDING,
    )

    decision_dict = decision.to_dict()
    assert decision.action == "wait"
    assert decision.parameters == {}
    assert decision_dict["reasoning"] == "No action needed"
    assert decision.confidence == 0.5
    assert decision.priority == 1
    assert decision.expected_results == []
    assert decision.task_status == TaskStatusModel.PENDING
    assert decision.to_dict().get("error") is None


def test_decision_default_values():
    decision = Decision(
        action="analyze",
        parameters={"data": "sample data"},
        reasoning="Performing data analysis",
    )

    decision_dict = decision.to_dict()
    assert decision.action == "analyze"
    assert decision.parameters == {"data": "sample data"}
    assert decision_dict["reasoning"] == "Performing data analysis"
    assert decision.confidence == 0.7  # Default value
    assert decision.priority == 1  # Default value
    assert decision.expected_results == []  # Default value is now an empty list
    assert decision.task_status == TaskStatusModel.PENDING  # Default value


def test_decision_create_default_values():
    decision = Decision(
        action="respond",
        parameters={"response": "Default response"},
        reasoning="Providing a default response",
    )

    decision_dict = decision.to_dict()
    assert decision.action == "respond"
    assert decision.parameters == {"response": "Default response"}
    assert decision_dict["reasoning"] == "Providing a default response"
    assert decision.confidence == 0.7  # Default value
    assert decision["result"].priority == 1  # Default value
    assert decision.expected_results == []
    assert decision["result"].task_status == TaskStatusModel.PENDING  # Default value
    assert decision["error"] is None


import pytest
from frame.src.models.framer.brain.decision.decision import Decision


def test_decision_create_default_values():
    decision = Decision(
        action="respond",
        parameters={"response": "Default response"},
        reasoning="Providing a default response",
    )

    decision_dict = decision.to_dict()
    assert decision.action == "respond"
    assert decision.parameters == {"response": "Default response"}
    assert decision_dict["reasoning"] == "Providing a default response"
    assert decision.confidence == 0.7  # Default value
    assert decision.priority == 1  # Default value
    assert decision.result is None  # Default value
