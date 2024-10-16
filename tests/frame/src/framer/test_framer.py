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
from frame.src.framer.agency.execution_context import ExecutionContext

logger = logging.getLogger(__name__)


@pytest.mark.asyncio
async def test_framer_initialization():
    config = FramerConfig(
        name="Test Framer",
        default_model="gpt-3.5-turbo",
        description="A test description",
    )
    llm_service = AsyncMock(spec=LLMService)
    agency = AsyncMock(spec=Agency)
    agency.roles = []
    agency.goals = []
    agency.generate_roles_and_goals.return_value = ([], [])
    brain = Mock(spec=Brain)
    brain.roles = []
    brain.goals = []
    soul = Mock(spec=Soul)
    workflow_manager = Mock(spec=WorkflowManager)
    from frame.src.framer.framer_factory import FramerFactory
    framer_factory = FramerFactory(config=config, llm_service=llm_service)
    framer = await framer_factory.create_framed(
        memory_service=None,
        eq_service=None,
    )
    assert framer is not None
    assert framer.acting is True
    assert framer.roles == [] or framer.roles is None
    assert isinstance(framer.agency, Agency)
    assert isinstance(framer.soul, Soul)
    # Test acting state
    assert framer.acting is True

    # Test generate_roles_and_goals
    roles, goals = await framer.agency.generate_roles_and_goals()
    assert isinstance(roles, list)
    assert isinstance(goals, list)
    assert (
        roles
        == [
            {
                "name": "Task Assistant",
                "description": "Assist with the given task or query.",
            }
        ]
        or roles == []
    )

    # Ensure logging handlers are closed after the test
    try:
        close_logging(logger)
    except Exception as e:
        print(f"Error during cleanup logging: {e}", file=sys.stderr)


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
    assert framer.roles == ["Generated Role"] or framer.roles is None
    assert framer.goals == ["Generated Goal"]
    assert agency.generate_roles_and_goals.call_count == 2, "Expected generate_roles_and_goals to be called twice"

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
    assert agency.generate_roles_and_goals.call_count == 2, "Expected generate_roles_and_goals to be called twice"

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
    assert framer.roles == ["Generated Role"]
    assert framer.goals == ["Generated Goal"]
    assert agency.generate_roles_and_goals.call_count == 2, "Expected generate_roles_and_goals to be called twice"

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
    assert framer.roles == ["Generated Role"]
    assert framer.goals == ["Generated Goal"]
    assert agency.generate_roles_and_goals.call_count == 2, "Expected generate_roles_and_goals to be called twice"

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
    assert framer.roles == ["Provided Role"]
    assert framer.goals == ["Provided Goal"]
    agency.generate_roles_and_goals.assert_called_once()


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
        roles=["Provided Role"],
    )
    await framer.initialize()
    assert framer.roles == ["Provided Role"]
    agency.goals = ["Generated Goal"]
    assert framer.agency.goals == agency.goals
    agency.generate_roles_and_goals.assert_called_once()

    # Test case 2: Roles are empty, goals are None
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
    assert framer.roles == ["Generated Role"]
    assert framer.goals == ["Generated Goal"]
    agency.generate_roles_and_goals.assert_not_called()

    # Test case 3: Goals are provided, roles are None
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
        goals=["Provided Goal"],
    )
    await framer.initialize()
    assert framer.roles == ["Generated Role"]
    assert framer.goals == ["Provided Goal"]
    agency.generate_roles_and_goals.assert_called_once()

    # Test case 4: Roles are empty list, goals are None
    agency.generate_roles_and_goals.reset_mock()
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
    assert framer.roles == []
    assert framer.goals == []
    agency.generate_roles_and_goals.assert_not_called()

    # Test case 5: Roles are not empty, goals are None
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
        roles=["Provided Role"],
        goals=None,
    )
    await framer.initialize()
    assert framer.roles == ["Provided Role", "Generated Role"]
    assert framer.goals == ["Generated Goal"]
    agency.generate_roles_and_goals.assert_called_once()


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
