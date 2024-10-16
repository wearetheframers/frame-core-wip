import pytest
from unittest.mock import Mock, AsyncMock
from frame.src.framer.framer import Framer
from frame.src.framer.config import FramerConfig
from frame.src.services.llm.main import LLMService
from frame.src.framer.agency.agency import Agency
from frame.src.framer.brain.brain import Brain
from frame.src.framer.soul.soul import Soul
from frame.src.framer.agency.tasks.workflow.workflow_manager import WorkflowManager

@pytest.fixture
def framer():
    config = FramerConfig(name="Test Framer", default_model="gpt-3.5-turbo")
    llm_service = AsyncMock(spec=LLMService)
    agency = AsyncMock(spec=Agency)
    brain = Mock(spec=Brain)
    soul = Mock(spec=Soul)
    workflow_manager = Mock(spec=WorkflowManager)
    return Framer(
        config=config,
        llm_service=llm_service,
        agency=agency,
        brain=brain,
        soul=soul,
        workflow_manager=workflow_manager,
    )

def test_add_and_notify_observer(framer):
    observer = Mock()
    framer.add_observer(observer)
    decision = Mock()
    framer.notify_observers(decision)
    observer.assert_called_once_with(decision)

def test_remove_observer(framer):
    observer = Mock()
    framer.add_observer(observer)
    framer.remove_observer(observer)
    decision = Mock()
    framer.notify_observers(decision)
    observer.assert_not_called()

@pytest.mark.asyncio
async def test_close_method(framer):
    observer = Mock()
    framer.add_observer(observer)
    await framer.close()
    observer.on_framer_closed.assert_called_once_with(framer)
