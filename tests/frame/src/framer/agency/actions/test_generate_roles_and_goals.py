import pytest
from unittest.mock import Mock
from frame.src.framer.agency.actions.generate_roles_and_goals import (
    generate_roles_and_goals,
)
from frame.src.framer.agency.execution_context import ExecutionContext


@pytest.fixture
def mock_framer():
    framer = Mock()
    framer.agency = Mock()
    framer.agency.generate_roles_and_goals.return_value = (
        [{"name": "Role 1", "description": "Description 1"}],
        [{"name": "Goal 1", "description": "Description 1"}],
    )
    return framer


def test_generate_roles_and_goals(mock_framer):
    result = generate_roles_and_goals(mock_framer)

    mock_framer.agency.generate_roles_and_goals.assert_called_once()
    mock_framer.agency.set_roles.assert_called_once()
    mock_framer.agency.set_goals.assert_called_once()

    assert isinstance(result, tuple)
    assert len(result) == 2
    roles, goals = result
    assert len(roles) == 1
    assert roles[0]["name"] == "Role 1"
    assert len(goals) == 1
    assert goals[0]["name"] == "Goal 1"
