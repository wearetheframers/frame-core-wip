import pytest
from frame.src.framer.brain.plugins.base import BasePlugin
from typing import Any


class TestPlugin(BasePlugin):
    def __init__(self, framer):
        super().__init__(framer)
        self.actions = {"test_action": self.test_action}

    async def on_load(self):
        pass

    async def on_remove(self):
        pass

    async def execute(self, action: str, params: dict, execution_context: Any) -> Any:
        return "Executed"

    def test_action(self):
        return "Test action executed"


def test_plugin_inheritance():
    framer_mock = object()  # Mock object for framer
    plugin = TestPlugin(framer_mock)
    assert isinstance(plugin, BasePlugin), "Plugin should inherit from BasePlugin"
    assert plugin.framer == framer_mock, "Framer should be set correctly"
    assert "test_action" in plugin.actions, "Plugin should have 'test_action'"


def test_plugin_action_execution():
    framer_mock = object()  # Mock object for framer
    plugin = TestPlugin(framer_mock)
    result = plugin.test_action()
    assert result == "Test action executed", "Action should execute correctly"
