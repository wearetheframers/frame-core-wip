import pytest
from frame.src.models.framer.brain.decision.decision import Decision
from frame.src.framer.agency.tasks.task_status import TaskStatus
from frame.src.framer.agency.priority import Priority


def test_decision_initialization():
    decision = Decision(
        action="respond",
        parameters={"response": "Hello, world!"},
        reasoning="Greeting the user",
        confidence=0.9,
        priority=5,
        task_status=TaskStatus.IN_PROGRESS,
    )

    assert decision.action == "respond"
    assert decision.parameters == {"response": "Hello, world!"}
    assert decision.reasoning == "Greeting the user"
    assert decision.confidence == 0.9
    assert decision.priority == 5
    assert decision.expected_results == []  # Default value is an empty list
    assert decision.task_status == TaskStatus.IN_PROGRESS


def test_decision_from_json():
    json_str = '{"action": "research", "parameters": {"topic": "AI"}, "reasoning": "Gather information", "confidence": 0.8, "priority": 7, "task_status": "in_progress"}'
    decision = Decision.parse_raw(json_str)

    assert decision.action == "research"
    assert decision.parameters == {"topic": "AI"}
    assert decision.reasoning == "Gather information"
    assert decision.confidence == 0.8
    assert decision.priority == 7
    assert decision.task_status == TaskStatus.IN_PROGRESS
    assert decision.expected_results == []  # Default is an empty list


def test_decision_to_dict():
    decision = Decision(
        action="generate_tasks",
        parameters={"tasks": ["Task 1", "Task 2"]},
        reasoning="Creating new tasks",
        confidence=0.7,
        priority=6,
        expected_results=["Completed Task 1", "Completed Task 2"],
        task_status=TaskStatus.COMPLETED,
    )

    decision_dict = decision.dict()

    assert decision_dict["action"] == "generate_tasks"
    assert decision_dict["parameters"] == {"tasks": ["Task 1", "Task 2"]}
    assert decision_dict["reasoning"] == "Creating new tasks"
    assert decision_dict["confidence"] == 0.7
    assert decision_dict["priority"] == 6
    assert decision_dict["task_status"] == TaskStatus.COMPLETED
    assert decision_dict["expected_results"] == ["Completed Task 1", "Completed Task 2"]


def test_decision_create():
    decision = Decision(
        action="wait",
        parameters={},
        reasoning="No action needed",
        confidence=0.5,
        priority=1,
        expected_results=[],  # Explicitly set an empty list
        task_status=TaskStatus.PENDING,
    )

    decision_dict = decision.dict()
    assert decision.action == "wait"
    assert decision.parameters == {}
    assert decision.reasoning == "No action needed"
    assert decision.confidence == 0.5
    assert decision.priority == 1
    assert decision.expected_results == []
    assert decision.task_status == TaskStatus.PENDING


def test_decision_default_values():
    decision = Decision(
        action="analyze",
        parameters={"data": "sample data"},
        reasoning="Performing data analysis",
    )

    decision_dict = decision.dict()
    assert decision.action == "analyze"
    assert decision.parameters == {"data": "sample data"}
    assert decision.reasoning == "Performing data analysis"
    assert decision.confidence == 0.7  # Default value
    assert decision.priority == Priority.MEDIUM.value  # Default value
    assert decision.expected_results == []  # Default value is now an empty list
    assert decision.task_status == TaskStatus.PENDING  # Default value


def test_decision_priority_validation():
    # Test with integer priority
    decision = Decision(action="test", priority=8)
    assert decision.priority == 8

    # Test with string priority
    decision = Decision(action="test", priority="HIGH")
    assert decision.priority == Priority.HIGH.value

    # Test with Priority enum
    decision = Decision(action="test", priority=Priority.LOW)
    assert decision.priority == Priority.LOW.value

    # Test with invalid string priority
    decision = Decision(action="test", priority="INVALID")
    assert decision.priority == Priority.MEDIUM.value

    # Test with out of range integer priority
    decision = Decision(action="test", priority=15)
    assert decision.priority == 10  # Should be capped at 10

    decision = Decision(action="test", priority=-1)
    assert decision.priority == 1  # Should be minimum 1
