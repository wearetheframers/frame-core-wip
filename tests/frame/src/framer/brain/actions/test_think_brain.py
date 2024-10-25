import unittest
from unittest.mock import AsyncMock, MagicMock
from frame.src.framer.brain.actions.think import ThinkAction
from frame.src.services import ExecutionContext

class TestThinkAction(unittest.IsolatedAsyncioTestCase):
    async def test_execute_think_action(self):
        execution_context = MagicMock(spec=ExecutionContext)
        execution_context.brain = MagicMock()
        execution_context.brain._execute_think_action = AsyncMock(return_value={"result": "success"})

        action = ThinkAction()
        result = await action.execute(execution_context, thought="Reflecting...")
        self.assertEqual(result, {"result": "success"})

    async def test_execute_think_action_no_brain(self):
        execution_context = MagicMock(spec=ExecutionContext)
        execution_context.brain = None

        action = ThinkAction()
        result = await action.execute(execution_context, thought="Reflecting...")
        self.assertEqual(result, {"error": "Brain not available in execution context"})

if __name__ == "__main__":
    unittest.main()
