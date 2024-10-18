import pytest
from frame.src.services import LocalContext


def test_context_initialization():
    context = LocalContext()
    assert context.roles == []
    assert context.goals == []
    assert context.soul is None
    assert context.state == {}


def test_context_initialization_with_soul():
    soul_mock = object()
    context = LocalContext(soul=soul_mock)
    assert context.soul == soul_mock


def test_get_set_roles():
    context = LocalContext()
    roles = [{"name": "Role1", "description": "Description1"}]
    context.set_roles(roles)
    assert context.get_roles() == roles


def test_get_set_goals():
    context = LocalContext()
    goals = [{"description": "Goal1", "priority": 1.0}]
    context.set_goals(goals)
    assert context.get_goals() == goals


def test_set_soul():
    context = LocalContext()
    soul_mock = object()
    context.set_soul(soul_mock)
    assert context.soul == soul_mock


def test_state_initialization():
    state = {"key": "value"}
    context = LocalContext(**state)
    assert context.state == state


def test_get_method():
    context = LocalContext(soul="test_soul", test_key="test_value")
    assert context.get("test_key") == "test_value"
    assert context.get("non_existent_key") is None
    assert context.get("non_existent_key", "default") == "default"


def test_setattr_and_getattr():
    context = LocalContext()
    context.new_attribute = "new_value"
    assert context.new_attribute == "new_value"
    assert context.get("new_attribute") == "new_value"

    with pytest.raises(AttributeError):
        _ = context.non_existent_attribute


def test_context_with_multiple_attributes():
    context = LocalContext(soul="test_soul", attr1="value1", attr2="value2")
    assert context.soul == "test_soul"
    assert context.attr1 == "value1"
    assert context.attr2 == "value2"
    assert context.state == {"attr1": "value1", "attr2": "value2"}
