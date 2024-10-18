import pytest
from unittest.mock import Mock
from frame.src.framed.config import FramedConfig
from frame.src.framed import Framed
from frame.src.framed.framed_factory import FramedFactory
from frame.src.services.llm.main import LLMService
from frame.src.services import ExecutionContext


@pytest.fixture
def mock_frame():
    return Mock()


@pytest.fixture
def mock_llm_service():
    return Mock()


@pytest.fixture
def framed_factory(mock_frame, mock_llm_service):
    config = FramedConfig(name="TestFramed")
    return FramedFactory(config, mock_llm_service)


def test_framed_factory_initialization(framed_factory, mock_frame, mock_llm_service):
    assert isinstance(framed_factory, FramedFactory)
    assert isinstance(framed_factory.llm_service, LLMService)


@pytest.mark.asyncio
async def test_create_framed(framed_factory):
    config = FramedConfig(name="TestFramed")
    roles = [{"name": "TestRole"}]
    goals = [{"description": "TestGoal"}]

    result = await framed_factory.create_framed(roles=roles, goals=goals)

    assert isinstance(result, Framed)
    # Add more assertions here once the create_framed method is fully implemented
