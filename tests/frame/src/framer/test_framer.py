import pytest
from frame.src.framer.framer import Framer
from frame.src.framer.config import FramerConfig
from frame.src.framer.brain.memory import Memory
from frame.src.framer.agency.tasks.workflow import WorkflowManager
from frame.src.framer.agency.tasks.workflow.workflow import Workflow
from frame.src.framer.brain.decision import Decision
from frame.src.utils.log_manager import close_logging
from frame.src.framer.agency.agency import Agency
from frame.src.services.llm.main import LLMService
from frame.src.framer.agency.tasks.task import Task, TaskStatus
from frame.src.framer.brain.brain import Brain
from frame.src.framer.soul.soul import Soul
from unittest.mock import Mock, AsyncMock, patch
import logging

logger = logging.getLogger(__name__)


@pytest.mark.asyncio
async def test_framer_initialization():
    config = FramerConfig(
        name="Test Framer",
        default_model="gpt-3.5-turbo",
        description="A test description",
        # Add other necessary configuration parameters here
    )
    llm_service = AsyncMock(spec=LLMService)
    agency = AsyncMock(spec=Agency)
    agency.roles = []
    agency.goals = []
    agency.generate_roles_and_goals.return_value = ([], [])
    agency.roles = []
    agency.goals = []
    agency.roles = []
    agency.goals = []
    agency.roles = []
    agency.goals = []
    agency.roles = []
    agency.goals = []
    agency.roles = []
    agency.goals = []
    agency.roles = []
    agency.goals = []
    agency.roles = []
    agency.goals = []
    brain = Mock(spec=Brain)
    brain.roles = []
    brain.goals = []
    agency.roles = []
    agency.goals = []
    agency.roles = []
    agency.goals = []
    agency.roles = []
    agency.goals = []
    soul = Mock(spec=Soul)
    workflow_manager = Mock(spec=WorkflowManager)
    framer = Framer(
        config=config,
        llm_service=llm_service,
        agency=agency,
        brain=brain,
        soul=soul,
        workflow_manager=workflow_manager,
    )
    assert framer is not None
    assert isinstance(framer.agency, Agency)
    assert isinstance(framer.soul, Soul)
    # Test generate_roles_and_goals
    roles, goals = await framer.agency.generate_roles_and_goals()
    assert isinstance(roles, list)
    assert isinstance(goals, list)

    # Ensure logging handlers are closed after the test
    close_logging(logger)


@pytest.mark.asyncio
async def test_framer_initialize():
    config = FramerConfig(
        name="Test Framer",
        default_model="gpt-3.5-turbo",
        description="A test description",
    )
    llm_service = AsyncMock(spec=LLMService)
    agency = AsyncMock(spec=Agency)
    brain = Mock(spec=Brain)
    soul = Mock(spec=Soul)
    workflow_manager = Mock(spec=WorkflowManager)

    # Test case 1: Both roles and goals are None
    agency.generate_roles_and_goals.return_value = (
        ["Generated Role"],
        ["Generated Goal"],
    )
    framer = Framer(
        config=config,
        llm_service=llm_service,
        agency=agency,
        brain=brain,
        soul=soul,
        workflow_manager=workflow_manager,
    )
    await framer.initialize()
    assert framer.roles == ["Generated Role"]
    assert framer.goals == ["Generated Goal"]
    agency.generate_roles_and_goals.assert_called_once()

    # Test case 2: Both roles and goals are empty lists
    agency.generate_roles_and_goals.reset_mock()
    agency.generate_roles_and_goals.return_value = (
        ["Generated Role"],
        ["Generated Goal"],
    )
    framer = Framer(
        config=config,
        llm_service=llm_service,
        agency=agency,
        brain=brain,
        soul=soul,
        workflow_manager=workflow_manager,
        roles=[],
        goals=[],
    )
    await framer.initialize()
    assert framer.roles == ["Generated Role"]
    assert framer.goals == ["Generated Goal"]
    agency.generate_roles_and_goals.assert_called_once()

    # Test case 3: Roles are None, goals are empty list
    agency.generate_roles_and_goals.reset_mock()
    agency.generate_roles_and_goals.return_value = (
        ["Generated Role"],
        ["Generated Goal"],
    )
    framer = Framer(
        config=config,
        llm_service=llm_service,
        agency=agency,
        brain=brain,
        soul=soul,
        workflow_manager=workflow_manager,
        roles=None,
        goals=[],
    )
    await framer.initialize()
    assert framer.agency.roles == ["Generated Role"]
    assert framer.agency.goals == []
    agency.generate_roles_and_goals.assert_called_once()

    # Test case 4: Roles are empty list, goals are None
    agency.generate_roles_and_goals.reset_mock()
    agency.generate_roles_and_goals.return_value = (
        ["Generated Role"],
        ["Generated Goal"],
    )
    framer = Framer(
        config=config,
        llm_service=llm_service,
        agency=agency,
        brain=brain,
        soul=soul,
        workflow_manager=workflow_manager,
        roles=[],
        goals=None,
    )
    await framer.initialize()
    assert framer.agency.roles == []
    assert framer.agency.goals == ["Generated Goal"]
    agency.generate_roles_and_goals.assert_called_once()

    # Test case 5: Both roles and goals are provided
    agency.generate_roles_and_goals.reset_mock()
    framer = Framer(
        config=config,
        llm_service=llm_service,
        agency=agency,
        brain=brain,
        soul=soul,
        workflow_manager=workflow_manager,
        roles=["Provided Role"],
        goals=["Provided Goal"],
    )
    await framer.initialize()
    assert framer.agency.roles == ["Provided Role"]
    assert framer.agency.goals == ["Provided Goal"]
    agency.generate_roles_and_goals.assert_not_called()


@pytest.mark.asyncio
async def test_framer_initialize_with_provided_values():
    config = FramerConfig(
        name="Test Framer",
        default_model="gpt-3.5-turbo",
        description="A test description",
    )
    llm_service = AsyncMock(spec=LLMService)
    agency = AsyncMock(spec=Agency)
    brain = Mock(spec=Brain)
    soul = Mock(spec=Soul)
    workflow_manager = Mock(spec=WorkflowManager)

    # Test case 1: Roles are provided, goals are None
    agency.generate_roles_and_goals.return_value = ([], ["Generated Goal"])
    framer = Framer(
        config=config,
        llm_service=llm_service,
        agency=agency,
        brain=brain,
        soul=soul,
        workflow_manager=workflow_manager,
        roles=["Provided Role"],
    )
    await framer.initialize()
    assert framer.agency.roles == ["Provided Role"]
    assert framer.agency.goals == ["Generated Goal"]

    # Test case 2: Goals are provided, roles are None
    agency.generate_roles_and_goals.return_value = (["Generated Role"], [])
    framer = Framer(
        config=config,
        llm_service=llm_service,
        agency=agency,
        brain=brain,
        soul=soul,
        workflow_manager=workflow_manager,
        goals=["Provided Goal"],
    )
    await framer.initialize()
    assert framer.roles == ["Generated Role"]
    assert framer.goals == ["Provided Goal"]


@pytest.mark.asyncio
async def test_cancel_task():
    config = FramerConfig(name="TestFramer")
    llm_service = Mock(spec=LLMService)
    framer = await Framer.create(config=config, llm_service=llm_service)

    # Create a task
    task = Task(description="Test task", workflow_id="default")
    framer.workflow_manager.add_task("default", task)

    # Cancel the task
    await framer.workflow_manager.cancel_task(task.id)

    # Check if the task status is CANCELED
    assert task.status == TaskStatus.CANCELED


def test_soul_seed_initialization():
    soul = Soul(seed={"seed": "Test soul seed"})
