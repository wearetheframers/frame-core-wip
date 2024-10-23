import pytest
from frame.src.services import ExecutionContext
from frame.src.services import LLMService
from frame.src.framer.soul import Soul
from frame.src.framer.config import FramerConfig


@pytest.fixture
def llm_service():
    return LLMService()


@pytest.fixture
def soul():
    return Soul()


def test_execution_context_service_initialization(llm_service, soul):
    execution_context = ExecutionContext(llm_service=llm_service, soul=soul)
    assert execution_context.get_llm_service() == llm_service
    assert execution_context.get_soul() == soul
    assert execution_context.get_state() == {}


def test_execution_context_service_update_state(llm_service, soul):
    execution_context = ExecutionContext(llm_service=llm_service, soul=soul)
    new_state = {"key": "value"}
    execution_context.update_state(new_state)
    assert execution_context.get_state() == new_state
    assert execution_context.get_state("key") == "value"


@pytest.mark.asyncio
async def test_execution_context_service_in_action_registry():
    execution_context = ExecutionContext(llm_service=llm_service)
    assert execution_context.get_soul() is None


@pytest.mark.asyncio
async def test_execution_context_service_in_action_registry():
    from frame.src.framer.brain.action_registry import ActionRegistry

    llm_service = LLMService()
    execution_context = ExecutionContext(llm_service=llm_service)
    action_registry = ActionRegistry(execution_context)

    async def test_action(execution_context, param):
        return {"response": f"Test action with param: {param}"}
        return f"Test action with param: {param}"

    action_registry.add_action(
        action_or_name="test_action",
        action_func=test_action,
        description="Test action description",
    )

    result = await action_registry.execute_action("test_action", param="test_value")
    assert result["response"] == "Test action with param: test_value"
