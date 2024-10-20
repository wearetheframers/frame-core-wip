import pytest
from unittest.mock import Mock, AsyncMock
from frame.src.framer.brain.actions.generate_roles_and_goals import (
    GenerateRolesAndGoalsAction,
)
from frame.src.services.execution_context import ExecutionContext


@pytest.fixture
def mock_execution_context():
    context = Mock(spec=ExecutionContext)
    context.framer = Mock()
    context.framer.agency = AsyncMock()
    context.framer.agency.generate_roles_and_goals.return_value = (
        [{"name": "Role 1", "description": "Description 1"}],
        [{"name": "Goal 1", "description": "Description 1"}],
    )
    return context


@pytest.mark.asyncio
async def test_generate_roles_and_goals(mock_execution_context):
    action = GenerateRolesAndGoalsAction(
        name="Generate Roles and Goals",
        description="Generate roles and goals for the framer",
    )
    result = await action.execute(mock_execution_context)

    mock_execution_context.framer.agency.generate_roles_and_goals.assert_called_once()
    mock_execution_context.framer.agency.set_roles.assert_called_once()
    mock_execution_context.framer.agency.set_goals.assert_called_once()

    assert isinstance(result, tuple)
    assert len(result) == 2
    roles, goals = result
    assert len(roles) == 1
    assert roles[0]["name"] == "Role 1"
    assert len(goals) == 1
    assert goals[0]["name"] == "Goal 1"
