import unittest
from unittest.mock import MagicMock
from frame.src.framer.brain.actions.error import ErrorAction
from frame.src.services import ExecutionContext


class TestErrorAction(unittest.IsolatedAsyncioTestCase):
    async def test_execute_error_action(self):
        execution_context = MagicMock(spec=ExecutionContext)
        execution_context.soul.get_current_state = MagicMock(return_value="Calm")
        execution_context.get_recent_thoughts = MagicMock(
            return_value=["Thought1", "Thought2"]
        )
        execution_context.roles = []
        execution_context.get_goals = MagicMock(return_value=[])

        action = ErrorAction()
        result = await action.execute(execution_context, error="Test error")
        self.assertIn("I apologize, an error occurred: Test error.", result["response"])


if __name__ == "__main__":
    unittest.main()
