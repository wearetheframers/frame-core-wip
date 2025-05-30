import pytest
import json
from unittest.mock import AsyncMock, MagicMock, patch, Mock
from frame.src.framed.config import FramedConfig
from frame.src.framed.framed import Framed
from frame.src.framer.soul.soul import Soul
from frame.src.framer.agency import Agency
from frame.src.framer.agency.roles import Role
from frame.src.framer.agency.goals import Goal
from frame.src.services.llm.main import LLMService
from frame.src.framer.agency.tasks.task import Task
from frame.src.framer.agency.workflow import Workflow
from frame.src.framer.agency.workflow.workflow_manager import WorkflowManager
from frame.src.framer.brain.brain import Brain
from frame.src.services import ExecutionContext


@pytest.fixture
def mock_llm_service():
    return AsyncMock(spec=LLMService)


@pytest.fixture
def agency(mock_llm_service):
    mock_execution_context = Mock()
    mock_execution_context.llm_service = mock_llm_service
    return Agency(
        llm_service=mock_llm_service,
        context={},
        execution_context=mock_execution_context,
    )


def test_agency_initialization(agency, mock_llm_service):
    assert agency.llm_service == mock_llm_service
    assert isinstance(agency.workflow_manager, WorkflowManager)
    assert agency.roles == []
    assert agency.goals == []
    print(f"Roles: {agency.roles}, Goals: {agency.goals}")
    assert agency.context is not None


@pytest.mark.asyncio
async def test_generate_roles_with_numeric_priority(agency):
    agency.llm_service.get_completion = AsyncMock()
    agency.llm_service.get_completion.return_value = (
        '{"name": "Role1", "description": "A test role", "priority": 9}'
    )
    roles = await agency.generate_roles()
    assert roles[0].name == "Role1"
    assert roles[0].description == "A test role"
    assert roles[0].priority == 9


async def test_generate_roles_with_string_priority(agency):
    agency.llm_service.get_completion = AsyncMock()
    agency.llm_service.get_completion.return_value = (
        '{"name": "Role1", "description": "A test role", "priority": "medium"}'
    )
    roles = await agency.generate_roles()
    assert roles[0]["parameters"] == {
        "name": "Role1",
        "description": "A test role",
        "priority": 5,
    }
    mock_roles = [{"name": "Test Role", "description": "A test role"}]
    mock_goals = [{"description": "Test Goal", "priority": 1}]

    with patch.object(agency, "generate_roles", return_value=mock_roles), patch.object(
        agency, "generate_goals", return_value=mock_goals
    ):
        roles, goals = await agency.generate_roles_and_goals()

    assert roles == mock_roles
    assert goals == mock_goals


def test_add_role(agency):
    role = Role(name="Test Role", description="A test role")
    agency.add_role(role)
    assert any(r.name == "Test Role" for r in agency.get_roles())


def test_add_goal(agency):
    goal = Goal(name="Test Goal", description="A test goal", priority=1)
    agency.add_goal(goal)
    assert any(g.name == "Test Goal" for g in agency.get_goals())


def test_get_roles(agency):
    role1 = {"name": "Role 1", "description": "First role"}
    role2 = {"name": "Role 2", "description": "Second role"}
    agency.roles = [role1, role2]
    assert agency.get_roles() == [role1, role2]


def test_get_goals(agency):
    goal1 = {"description": "Goal 1", "priority": 1}
    goal2 = {"description": "Goal 2", "priority": 2}
    agency.goals = [goal1, goal2]
    assert agency.get_goals() == [goal1, goal2]


def test_create_task_with_numeric_priority(agency):
    task = agency.create_task("Test task", priority=7, workflow_id="test_workflow")
    assert isinstance(task, Task)
    assert task.description == "Test task"
    assert task.priority == 7
    assert task.workflow_id == "test_workflow"


def test_create_task_with_string_priority(agency):
    task = agency.create_task("Test task", priority="high", workflow_id="test_workflow")
    assert task.priority == 8


def test_create_task_with_invalid_priority(agency):
    with pytest.raises(ValueError):
        agency.create_task("Test task", priority=11, workflow_id="test_workflow")


@pytest.mark.parametrize(
    "task_data, workflow_name",
    [
        ({"description": "Task 1", "priority": 5}, "default"),
        ({"description": "Task 2", "priority": 8}, "custom_workflow"),
        ({"description": "Task 3"}, "default"),
    ],
)
def test_add_task(agency, task_data, workflow_name):
    task = agency.create_task(**task_data, workflow_id=workflow_name)
    agency.add_task(task, workflow_name)
    workflow = agency.workflow_manager.get_workflow(workflow_name)
    assert workflow is not None
    tasks = [t for t in workflow.tasks if t.description == task_data["description"]]
    assert len(tasks) == 1
    assert tasks[0].priority == task_data.get("priority", 5)  # Default priority is 5


@pytest.mark.asyncio
async def test_framed_can_execute(mock_llm_service):
    config = FramedConfig(name="Test Framed")
    agency = Mock(spec=Agency)
    brain = Mock(spec=Brain)
    soul = Mock(spec=Soul)
    workflow_manager = Mock(spec=WorkflowManager)
    framed = Framed(
        config=config,
        llm_service=mock_llm_service,
        agency=agency,
        brain=brain,
        soul=soul,
        workflow_manager=workflow_manager,
    )
    brain.framed = framed


def test_get_all_tasks(agency):
    workflow1 = agency.create_workflow("Workflow 1")
    workflow2 = agency.create_workflow("Workflow 2")
    task1 = Task(description="Task 1", workflow_id=workflow1.id)
    task2 = Task(description="Task 2", workflow_id=workflow2.id)
    workflow1.add_task(task1)
    workflow2.add_task(task2)

    all_tasks = agency.get_all_tasks()
    assert len(all_tasks) == 2
    assert all_tasks[0]["description"] == "Task 1"
    assert all_tasks[1]["description"] == "Task 2"


@pytest.mark.asyncio
async def test_generate_roles_and_goals(agency):
    # Mock the context and soul
    agency.context = {"soul": "Test soul"}

    # Mock the generate_roles and generate_goals methods
    agency.llm_service.get_completion = AsyncMock()
    agency.llm_service.get_completion.return_value = '{"id": "role_1", "name": "Task Assistant", "description": "Assist with the given task or query.", "permissions": [], "priority": 5, "status": "ACTIVE"}'

    roles, goals = await agency.generate_roles_and_goals()

    assert roles == [
        {
            "name": "Task Assistant",
            "description": "Assist with the given task or query.",
        }
    ]
    assert goals == [{"description": "Test Goal", "priority": 1}]

    assert agency.generate_roles.call_count == 1
    assert agency.generate_goals.call_count == 1


@pytest.mark.asyncio
async def test_generate_roles_and_goals_empty_response(agency):
    # Mock the context and soul
    agency.context = {"soul": "Test soul"}

    # Mock the generate_roles and generate_goals methods to return empty responses
    agency.generate_roles = AsyncMock(
        return_value=[
            Role(
                name="Task Assistant",
                description="Assist with the given task or query.",
            )
        ]
    )
    agency.generate_goals = AsyncMock(
        return_value=[
            Goal(
                name="User Assistant",
                description="Assist users to the best of my abilities",
                priority=1,
            )
        ]
    )

    roles, goals = await agency.generate_roles_and_goals()

    assert roles == [
        Role(
            name="Task Assistant",
            description="Assist with the given task or query.",
            permissions=[],
        )
    ]
    assert goals == [
        Goal(
            name="User Assistant",
            description="Assist users to the best of my abilities",
            priority=1,
        )
    ]

    agency.generate_roles.assert_called_once()
    agency.generate_goals.assert_called_once()
