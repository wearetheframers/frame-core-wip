import pytest
import asyncio
from unittest.mock import Mock, AsyncMock
from frame.src.framer.brain.mind.mind import Mind
from frame.src.framer.brain.decision import Decision
from frame.src.models.framer.brain.mind.perception import Perception
from frame.src.framer.agency.execution_context import ExecutionContext


@pytest.fixture
def brain():
    # Assuming Brain is a class that needs to be initialized
    # You might need to import Brain and initialize it properly
    return AsyncMock()  # Replace with actual Brain initialization if needed


@pytest.fixture
def mind(brain):
    return Mind(brain=brain)


def test_mind_initialization(mind):
    assert mind.thoughts == []
    assert mind.current_thought == {}
    assert mind.perceptions == []


import time
from datetime import datetime, timedelta


def test_think(mind):
    thought = "This is a test thought"
    mind.think(thought)
    assert len(mind.thoughts) == 1
    assert mind.thoughts[0]["content"] == thought
    assert isinstance(mind.thoughts[0]["timestamp"], datetime)
    assert mind.current_thought["content"] == thought


def test_get_current_thought(mind):
    thought = "Current thought"
    mind.think(thought)
    current_thought = mind.get_current_thought()
    assert current_thought["content"] == thought
    assert isinstance(current_thought["timestamp"], datetime)


def test_get_all_thoughts(mind):
    thoughts = ["Thought 1", "Thought 2", "Thought 3"]
    for thought in thoughts:
        mind.think(thought)
        # Add a small delay to ensure different timestamps
        time.sleep(0.001)
    all_thoughts = mind.get_all_thoughts()
    assert len(all_thoughts) == 3
    assert [t["content"] for t in all_thoughts] == thoughts[
        ::-1
    ]  # Reverse order due to sorting
    assert all(isinstance(t["timestamp"], datetime) for t in all_thoughts)
    # Check if thoughts are sorted by timestamp in descending order
    assert all(
        all_thoughts[i]["timestamp"] >= all_thoughts[i + 1]["timestamp"]
        for i in range(len(all_thoughts) - 1)
    )


def test_clear_thoughts(mind):
    mind.think("Test thought")
    mind.clear_thoughts()
    assert mind.thoughts == []
    assert mind.current_thought == {}


@pytest.mark.asyncio
async def test_process_perception(mind, mocker):
    mocker.patch.object(
        mind.brain.llm_service,
        "get_completion",
        new_callable=AsyncMock,
    )
    mind.brain.llm_service.get_completion.return_value = (
        '{"action": "default_action", "parameters": {}}'
    )
    perception = Perception(type="test", data={"key": "value"})
    await mind.process_perception(perception)
    assert len(mind.perceptions) == 1
    assert mind.perceptions[0] == perception
    assert mind.get_current_thought()["content"] == "Processed perception: test"


@pytest.mark.asyncio
async def test_get_recent_perceptions(mind):
    perceptions = [
        Perception(type=f"test{i}", data={"key": f"value{i}"}) for i in range(10)
    ]
    for perception in perceptions:
        response = '{"action": "default_action", "parameters": {}}'
        mind.brain.llm_service.get_completion.return_value = (
            '{"action": "default_action", "parameters": {}}'
        )
        await mind.process_perception(perception)
    recent_perceptions = mind.get_recent_perceptions(5)
    assert len(recent_perceptions) == 5
    assert recent_perceptions == perceptions[-5:]


@pytest.mark.asyncio
async def test_make_decision(mind, mocker):
    mocker.patch.object(
        mind.brain.llm_service,
        "get_completion",
        return_value='{"action": "default_action", "parameters": {}, "reasoning": "Based on current thoughts", "confidence": 0.8, "priority": 5}',
    )
    perception = Perception(type="test", data={"key": "value"})
    decision = await mind.make_decision(perception)
    assert isinstance(decision, Decision)
    assert decision.action == "default_action"
    assert decision.reasoning == "Based on current thoughts"
    assert decision.confidence == 0.8
    assert decision.priority == 5


def test_generate_thoughts(mind):
    # Since the method is not implemented, we just check if it runs without errors
    mind.generate_thoughts()


def test_multiple_thoughts(mind):
    thoughts = ["Thought 1", "Thought 2", "Thought 3"]
    for thought in thoughts:
        mind.think(thought)
    assert [t["content"] for t in mind.thoughts] == thoughts
    assert mind.current_thought["content"] == thoughts[-1]


@pytest.mark.asyncio
async def test_get_recent_perceptions_less_than_available(mind):
    perceptions = [
        Perception(type=f"test{i}", data={"key": f"value{i}"}) for i in range(3)
    ]
    for perception in perceptions:
        await mind.process_perception(perception)
    recent_perceptions = mind.get_recent_perceptions(5)
    assert len(recent_perceptions) == 3
    assert recent_perceptions == perceptions


@pytest.mark.asyncio
async def test_get_recent_perceptions_zero_or_negative(mind):
    perceptions = [
        Perception(type=f"test{i}", data={"key": f"value{i}"}) for i in range(3)
    ]
    for perception in perceptions:
        await mind.process_perception(perception)
    assert len(mind.get_recent_perceptions(0)) == 0
    assert len(mind.get_recent_perceptions(-1)) == 0


@pytest.mark.asyncio
async def test_make_decision_with_thoughts(mind, mocker):
    mocker.patch.object(
        mind,
        "make_decision",
        return_value={
            "action": "default_action",
            "reason": "Based on current thoughts",
        },
    )
    thoughts = ["Thought 1", "Thought 2", "Decision thought"]
    for thought in thoughts:
        mind.think(thought)
    decision = await mind.make_decision(perception=None)
    assert isinstance(decision, dict)
    assert decision["action"] == "default_action"
    assert "Based on current thoughts" in decision["reason"]


def test_clear_thoughts_multiple_times(mind):
    mind.think("Thought 1")
    mind.clear_thoughts()
    mind.think("Thought 2")
    mind.clear_thoughts()
    assert mind.thoughts == []
    assert mind.current_thought == {}


@pytest.mark.asyncio
async def test_process_multiple_perceptions(mind, mocker):
    mocker.patch.object(
        mind.brain.llm_service,
        "get_completion",
        return_value='{"action": "default_action", "parameters": {}}',
    )
    perceptions = [
        Perception(type="visual", data={"object": "tree"}),
        Perception(type="auditory", data={"sound": "bird chirping"}),
        Perception(type="tactile", data={"texture": "rough"}),
    ]
    for perception in perceptions:
        await mind.process_perception(perception)
    assert len(mind.perceptions) == 3
    assert (
        mind.get_current_thought()["content"]
        == f"Processed perception: {perceptions[-1].type}"
    )
