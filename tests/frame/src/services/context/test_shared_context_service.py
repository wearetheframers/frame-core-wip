import pytest
from unittest.mock import MagicMock
from frame.src.services import SharedContext


def test_shared_context_initialization():
    llm_service = MagicMock()  # Mock the llm_service
    shared_context = SharedContext(llm_service=llm_service)
    assert shared_context.roles == []
    assert shared_context.goals == []
    assert shared_context.soul is None
    assert shared_context.state == {}


def test_shared_context_inheritance():
    llm_service = MagicMock()  # Mock the llm_service
    shared_context = SharedContext(llm_service=llm_service)
    assert isinstance(shared_context, SharedContext)


def test_shared_context_get_set_roles():
    llm_service = MagicMock()  # Mock the llm_service
    shared_context = SharedContext(llm_service=llm_service)
    roles = [{"name": "SharedRole1", "description": "SharedDescription1"}]
    shared_context.set_roles(roles)
    assert shared_context.get_roles() == roles


def test_shared_context_get_set_goals():
    llm_service = MagicMock()  # Mock the llm_service
    shared_context = SharedContext(llm_service=llm_service)
    goals = [{"description": "SharedGoal1", "priority": 1.0}]
    shared_context.set_goals(goals)
    assert shared_context.get_goals() == goals


def test_shared_context_set_soul():
    llm_service = MagicMock()  # Mock the llm_service
    shared_context = SharedContext(llm_service=llm_service)
    soul_mock = object()
    shared_context.soul = soul_mock
    assert shared_context.soul == soul_mock


def test_shared_context_state_initialization():
    state = {"shared_key": "shared_value"}
    llm_service = MagicMock()  # Mock the llm_service
    shared_context = SharedContext(llm_service=llm_service)
    shared_context.state = state
    assert shared_context.state == state
