import unittest
from unittest.mock import MagicMock
from frame.src.framer.brain.plugins.base import BasePlugin
from frame.src.framer.agency.priority import Priority


class TestBasePlugin(unittest.TestCase):
    def setUp(self):
        self.framer_mock = MagicMock()
        self.plugin = BasePlugin(self.framer_mock)

    def test_add_action(self):
        def think_action(params):
            return "Thinking..."

        self.plugin.add_action(
            "think", think_action, "Think about something", Priority.HIGH
        )
        actions = self.plugin.get_actions()
        self.assertIn("think", actions)
        self.assertEqual(actions["think"]["description"], "Think about something")

    def test_execute_think_action(self):
        def think_action(params):
            return "Thinking..."

        self.plugin.add_action(
            "think", think_action, "Think about something", Priority.HIGH
        )
        result = self.plugin.actions["think"]["action_func"]({})
        self.assertEqual(result, "Thinking...")

    def test_add_research_action(self):
        def research_action(params):
            return "Researching..."

        self.plugin.add_action(
            "research", research_action, "Research a topic", Priority.MEDIUM
        )
        actions = self.plugin.get_actions()
        self.assertIn("research", actions)
        self.assertEqual(actions["research"]["description"], "Research a topic")

    def test_execute_research_action(self):
        def research_action(params):
            return "Researching..."

        self.plugin.add_action(
            "research", research_action, "Research a topic", Priority.MEDIUM
        )
        result = self.plugin.actions["research"]["action_func"]({})
        self.assertEqual(result, "Researching...")


if __name__ == "__main__":
    unittest.main()
