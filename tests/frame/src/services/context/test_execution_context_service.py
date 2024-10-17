import pytest
from frame.src.services.context.execution_context_service import ExecutionContextService
from frame.src.services.llm.main import LLMService
from frame.src.framer.soul.soul import Soul

@pytest.fixture
def llm_service():
    return LLMService()

@pytest.fixture
def soul():
    return Soul()

def test_execution_context_service_initialization(llm_service, soul):
    execution_context = ExecutionContextService(llm_service=llm_service, soul=soul)
    assert execution_context.get_llm_service() == llm_service
    assert execution_context.get_soul() == soul
    assert execution_context.get_state() == {}

def test_execution_context_service_update_state(llm_service, soul):
    execution_context = ExecutionContextService(llm_service=llm_service, soul=soul)
    new_state = {"key": "value"}
    execution_context.update_state(new_state)
    assert execution_context.get_state() == new_state

def test_execution_context_service_without_soul(llm_service):
    execution_context = ExecutionContextService(llm_service=llm_service)
    assert execution_context.get_soul() is None

@pytest.mark.asyncio
async def test_execution_context_service_in_action_registry():
    from frame.src.framer.agency.action_registry import ActionRegistry
    
    llm_service = LLMService()
    execution_context = ExecutionContextService(llm_service=llm_service)
    action_registry = ActionRegistry(execution_context)
    
    def test_action(execution_context, param):
        return f"Test action with param: {param}"
    
    action_registry.register_action("test_action", test_action, "Test action description")
    
    result = await action_registry.execute_action("test_action", {"param": "test_value"})
    assert result == "Test action with param: test_value"
