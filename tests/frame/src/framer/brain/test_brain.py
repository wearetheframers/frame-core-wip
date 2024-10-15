import pytest
from unittest.mock import patch, AsyncMock, call, Mock
from frame.src.framer.brain.brain import Brain
from frame.src.framer.brain.decision import Decision
from frame.src.framer.brain.memory import Memory
from frame.src.framer.brain.mind import Mind
from frame.src.framer.brain.perception import Perception
from frame.src.framed.config import FramedConfig
from frame.src.framer.agency.execution_context import ExecutionContext


from unittest.mock import Mock


@pytest.fixture
def brain():
    mock_llm_service = AsyncMock()
    mock_llm_service.default_model = "gpt-3.5-turbo"
    default_model = "gpt-3.5-turbo"
    roles = []
    goals = []
    mock_agency = AsyncMock()
    mock_agency.perform_task = AsyncMock()

    with patch("frame.src.framer.brain.brain.Agency", return_value=mock_agency):
        brain = Brain(
            llm_service=mock_llm_service,
            roles=roles,
            goals=goals,
            default_model=default_model,
        )
    return brain


@pytest.fixture
def mock_llm_service():
    llm_service = AsyncMock()
    llm_service.get_completion.return_value = '{"action": "test_action", "parameters": {}, "reasoning": "Test reasoning", "confidence": 0.9, "priority": 1}'
    return llm_service


def test_framed_initialization():
    config = FramedConfig(name="TestFramed")
    assert config.name == "TestFramed"


def test_brain_initialization(brain):
    assert isinstance(brain.memory, Memory)
    assert isinstance(brain.mind, Mind)


@pytest.mark.asyncio
async def test_process_perception(brain):
    perception = Perception(type="visual", data={"object": "tree"})
    brain.action_registry.register_action(
        "test_action", AsyncMock(), description="Test action"
    )
    with patch.object(
        brain.llm_service, "get_completion", new_callable=AsyncMock
    ) as mock_get_completion:
        mock_get_completion.return_value = '{"action": "test_action", "parameters": {}, "reasoning": "Test reasoning", "confidence": 0.9, "priority": 1}'
        decision = await brain.process_perception(perception)
    assert len(brain.mind.perceptions) == 1
    assert brain.mind.perceptions[0] == perception
    assert isinstance(decision, Decision)
    assert decision.action == "test_action"


@pytest.mark.asyncio
async def test_make_decision(brain):
    # Register a mock action in the action registry
    brain.action_registry.register_action(
        "test_action", AsyncMock(), description="A test action", priority=1
    )
    with patch.object(
        brain.llm_service, "get_completion", new_callable=AsyncMock
    ) as mock_get_completion:
        mock_get_completion.return_value = '{"action": "test_action", "parameters": {}, "reasoning": "Test reasoning", "confidence": 0.9, "priority": 1}'
        perception = Perception(type="test", data={"key": "value"})
        decision = await brain.make_decision(perception)
    assert isinstance(decision, Decision)
    print(f"Decision: {decision}")
    # Convert decision to a JSON-serializable format
    decision_dict = (
        decision.to_dict() if hasattr(decision, "to_dict") else decision.__dict__
    )
    assert isinstance(decision_dict, dict)
    assert decision.action in brain.action_registry.actions
    assert decision.reasoning
    assert decision.expected_results == []  # Default value is an empty list


@pytest.mark.asyncio
async def test_make_decision_invalid_action(brain, caplog):
    with patch.object(
        brain.llm_service, "get_completion", new_callable=AsyncMock
    ) as mock_get_completion:
        mock_get_completion.return_value = '{"action": "invalid_action", "parameters": {}, "reasoning": "Test reasoning", "confidence": 0.9, "priority": 1}'
        perception = Perception(type="test", data={"key": "value"})
        decision = await brain.make_decision(perception)

    assert isinstance(decision, Decision)
    assert decision.action == "error"
    assert (
        "Invalid action 'invalid_action' was generated" in decision.reasoning
        or "Defaulted to 'error'" in decision.reasoning
    )
    assert "Defaulted to 'error'" in decision.reasoning
    assert isinstance(decision.parameters, dict)


def test_framed_create_method():
    config = FramedConfig(name="TestFramed")
    assert config.name == "TestFramed"


def test_update_memory(brain):
    brain.memory.update_memory("test_memory", "This is a test memory")
    assert brain.memory.get_core_memory("test_memory") == "This is a test memory"


def test_retrieve_memory(brain):
    brain.memory.update_memory("test_memory", "This is a test memory")
    retrieved_memory = brain.memory.retrieve_memory("test_memory")
    assert retrieved_memory == "This is a test memory"


@pytest.mark.asyncio
async def test_think(brain):
    brain.mind.think("This is a test thought")
    assert brain.mind.thoughts[-1]["content"] == "This is a test thought"


@pytest.mark.asyncio
async def test_get_current_thought(brain):
    brain.mind.think("This is a test thought")
    current_thought = brain.mind.get_current_thought()
    assert current_thought["content"] == "This is a test thought"


@pytest.mark.asyncio
async def test_get_all_thoughts(brain):
    thoughts = ["Thought 1", "Thought 2", "Thought 3"]
    for thought in thoughts:
        brain.mind.think(thought)
    assert [t["content"] for t in brain.mind.get_all_thoughts()] == thoughts


def test_clear_thoughts(brain):
    brain.mind.think("This is a test thought")
    brain.mind.clear_thoughts()
    assert brain.mind.get_all_thoughts() == []
    assert brain.mind.get_current_thought() == {}


@pytest.mark.asyncio
async def test_get_recent_perceptions_less_than_available(brain, mock_llm_service):
    brain.llm_service = mock_llm_service
    perceptions = [
        Perception(type=f"test{i}", data={"key": f"value{i}"}) for i in range(5)
    ]
    for perception in perceptions:
        await brain.process_perception(perception)
    recent_perceptions = brain.mind.get_recent_perceptions(3)
    assert len(recent_perceptions) == 3
    assert recent_perceptions == perceptions[-3:]


@pytest.mark.asyncio
async def test_get_recent_perceptions_zero_or_negative(brain, mock_llm_service):
    brain.llm_service = mock_llm_service
    perceptions = [
        Perception(type=f"test{i}", data={"key": f"value{i}"}) for i in range(5)
    ]
    for perception in perceptions:
        await brain.process_perception(perception)

    recent_perceptions = brain.mind.get_recent_perceptions(0)
    assert len(recent_perceptions) == 0

    recent_perceptions = brain.mind.get_recent_perceptions(-1)
    assert len(recent_perceptions) == 0


@pytest.mark.asyncio
async def test_framer_can_execute(brain):
    brain.framer = Mock()  # Mock the framer attribute
    brain.framer.can_execute = True
    with patch.object(
        brain, "execute_decision", new_callable=AsyncMock
    ) as mock_execute_decision:
        with patch.object(
            brain.llm_service, "get_completion", new_callable=AsyncMock
        ) as mock_get_completion:
            mock_get_completion.return_value = '{"action": "respond", "parameters": {}, "reasoning": "Test reasoning", "confidence": 0.9, "priority": 1}'
            perception = Perception(type="test", data={"key": "value"})
            response = await brain.process_perception(perception)
            assert isinstance(response, Decision)
            print("Perception Response:", response.to_dict())
        mock_execute_decision.assert_called_once()

    brain.framer.can_execute = False
    with patch.object(
        brain, "execute_decision", new_callable=AsyncMock
    ) as mock_execute_decision:
        with patch.object(
            brain.llm_service, "get_completion", new_callable=AsyncMock
        ) as mock_get_completion:
            mock_get_completion.return_value = '{"action": "respond", "parameters": {}, "reasoning": "Test reasoning", "confidence": 0.9, "priority": 1}'
            perception = Perception(type="test", data={"key": "value"})
            await brain.process_perception(perception)
            mock_execute_decision.assert_not_called()


def test_search_memories(brain):
    brain.memory.update_memory("memory1", "This is the first test memory")
    brain.memory.update_memory("memory2", "This is the second test memory")
    results = brain.memory.search_memories("first")
    assert len(results) == 1
    assert "first test memory" in results[0]["memory"]


@pytest.mark.asyncio
async def test_execute_decision(brain):
    decision = Decision(action="test_action", parameters={}, reasoning="Test reasoning")
    brain.action_registry.register_action(
        "test_action", AsyncMock(), description="Test action"
    )

    with patch.object(
        brain.action_registry, "execute_action", new_callable=AsyncMock
    ) as mock_execute_action:
        await brain.execute_decision(decision)
        mock_execute_action.assert_called_once_with("test_action", decision.parameters)


@pytest.mark.asyncio
async def test_execute_decision_think_action(brain):
    decision = Decision(
        action="think", parameters={"topic": "AI"}, reasoning="Thinking about AI"
    )
    brain.action_registry.register_action(
        "think", AsyncMock(), description="Think action"
    )

    with patch.object(
        brain, "_execute_think_action", new_callable=AsyncMock
    ) as mock_execute_think_action:
        mock_execute_think_action.return_value = {
            "analysis": "AI is advancing rapidly",
            "new_tasks": [],
            "generate_new_prompt": False,
            "new_prompt": "",
        }
        await brain.execute_decision(decision)
        mock_execute_think_action.assert_called_once_with(decision)


@pytest.mark.asyncio
async def test_generate_new_query(brain):
    decision = Decision(
        action="think", parameters={"topic": "AI"}, reasoning="Thinking about AI"
    )
    with patch.object(
        brain.llm_service, "get_completion", new_callable=AsyncMock
    ) as mock_get_completion:
        mock_get_completion.return_value = "What are the ethical implications of AI?"
        new_query = await brain._generate_new_query(decision)
        assert new_query == "What are the ethical implications of AI?"
        mock_get_completion.assert_called_once()
