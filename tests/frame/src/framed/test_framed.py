import pytest
from frame.src.framed import Framed, FramedConfig
from frame.src.framer.config import FramerConfig
from frame.src.services.llm.main import LLMService
from frame.src.framer.agency.agency import Agency
from frame.src.framer.brain.brain import Brain
from frame.src.framer.soul.soul import Soul
from frame.src.framed.framed_factory import FramedFactory
from frame.src.framer.agency.workflow.workflow_manager import WorkflowManager
from frame.src.services.context.execution_context_service import ExecutionContext


def test_framed_initialization():
    config = FramedConfig(name="TestFramed")
    llm_service = LLMService()
    agency = Agency(llm_service=llm_service, context={})
    brain = Brain(llm_service=llm_service, roles=[], goals=[])
    soul = Soul()
    workflow_manager = WorkflowManager()
    framed = Framed(config, llm_service, agency, brain, soul, workflow_manager)
    assert framed is not None
    # Add more assertions based on Framed's attributes and methods


import pytest
from frame.src.framed.framed import Framed


def test_framed_initialization():
    config = FramedConfig(name="TestFramed")
    llm_service = LLMService()
    agency = Agency(llm_service=llm_service, context={})
    brain = Brain(llm_service=llm_service, roles=[], goals=[])
    soul = Soul()
    workflow_manager = WorkflowManager()
    framed = Framed(config, llm_service, agency, brain, soul, workflow_manager)
    assert isinstance(framed, Framed)


@pytest.mark.asyncio
async def test_framed_create_method():
    config = FramedConfig(name="TestFramed")
    llm_service = LLMService()
    execution_context = ExecutionContext(llm_service=llm_service)
    agency = Agency(
        llm_service=llm_service, context={}, execution_context=execution_context
    )
    brain = Brain(
        llm_service=llm_service, roles=[], goals=[], execution_context=execution_context
    )
    soul = Soul()
    workflow_manager = WorkflowManager()
    framed_factory = FramedFactory(config, llm_service)
    framed = await framed_factory.create_framer()
    assert isinstance(framed, Framed)
    # Add more assertions based on Framed's attributes and methods
