import pytest
from frame.src.services import SharedContext


def test_shared_context_initialization():
    shared_context = SharedContext()
    assert shared_context.roles == []
    assert shared_context.goals == []
    assert shared_context.soul is None
    assert shared_context.state == {}


def test_shared_context_inheritance():
    shared_context = SharedContext()
    assert isinstance(shared_context, SharedContext)


def test_shared_context_get_set_roles():
    shared_context = SharedContext()
    roles = [{"name": "SharedRole1", "description": "SharedDescription1"}]
    shared_context.set_roles(roles)
    assert shared_context.get_roles() == roles


def test_shared_context_get_set_goals():
    shared_context = SharedContext()
    goals = [{"description": "SharedGoal1", "priority": 1.0}]
    shared_context.set_goals(goals)
    assert shared_context.get_goals() == goals


def test_shared_context_set_soul():
    shared_context = SharedContext()
    soul_mock = object()
    shared_context.set_soul(soul_mock)
    assert shared_context.soul == soul_mock


def test_shared_context_state_initialization():
    state = {"shared_key": "shared_value"}
    shared_context = SharedContext(**state)
    assert shared_context.state == state
