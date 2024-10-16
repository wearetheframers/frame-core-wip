import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from frame.src.framed.framed_factory import FramedFactory
from frame.src.framer.framer_factory import FramerBuilder
from frame.src.framer.config import FramerConfig
from frame.src.services.llm.main import LLMService
from frame.src.framer.agency.execution_context import ExecutionContext


@pytest.fixture
def mock_llm_service():
    return AsyncMock(spec=LLMService)


@pytest.fixture
def framer_builder(mock_llm_service):
    config = FramerConfig(name="Test Framer", default_model="gpt-3.5-turbo")
    return FramerBuilder(config, mock_llm_service)


@pytest.mark.asyncio
async def test_create_framer(framer_builder):
    framer = await framer_builder.build()

    assert framer is not None
    assert framer.config.name == "Test Framer"
    assert framer.config.default_model == "gpt-3.5-turbo"


def test_framer_builder_set_config(framer_builder):
    new_config = FramerConfig(name="New Framer", default_model="gpt-4")
    framer_builder.config = new_config

    assert framer_builder.config.name == "New Framer"
    assert framer_builder.config.default_model == "gpt-4"


@pytest.mark.asyncio
async def test_framer_builder_build(framer_builder):
    framer = await framer_builder.build()

    assert framer is not None
    assert callable(framer.agency.perform_task)
    assert asyncio.iscoroutinefunction(framer.agency.perform_task)


@pytest.mark.asyncio
async def test_framer_builder_with_invalid_config():
    with pytest.raises(ValueError, match="Config must be an instance of FramerConfig"):
        FramerBuilder(
            config="Invalid Config",  # Pass an invalid config type
            llm_service=AsyncMock(),  # Use AsyncMock for LLMService
        )


@pytest.mark.asyncio
async def test_framer_builder_create_framer_without_soul_seed(framer_builder):
    framer = await framer_builder.build()

    assert framer.soul.seed is not None
    assert framer.soul.model.seed["text"] == "You are a helpful AI assistant."


@pytest.mark.asyncio
async def test_generate_roles_and_goals(framer_builder):
    framer = await framer_builder.build()
    with patch.object(
        framer.agency, "generate_roles_and_goals", new_callable=AsyncMock
    ) as mock_generate:
        mock_generate.return_value = (["Test Role"], ["Test Goal"])
        roles, goals = await framer.agency.generate_roles_and_goals()
        assert isinstance(roles, list)
        assert isinstance(goals, list)
        assert roles == ["Test Role"]
        assert goals == ["Test Goal"]
