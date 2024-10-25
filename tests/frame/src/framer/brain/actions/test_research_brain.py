import unittest
from unittest.mock import AsyncMock, MagicMock
from frame.src.framer.brain.actions.research import ResearchAction
from frame.src.services import ExecutionContext

class TestResearchAction(unittest.IsolatedAsyncioTestCase):
    async def test_execute_research_action(self):
        execution_context = MagicMock(spec=ExecutionContext)
        execution_context.llm_service = MagicMock()
        execution_context.llm_service.get_completion = AsyncMock(return_value="Research result")
        execution_context.memory_service = MagicMock()
        execution_context.memory_service.add_memory = AsyncMock()

        action = ResearchAction()
        result = await action.execute(execution_context, research_topic="AI")
        self.assertEqual(result["findings"], "Research result")

    async def test_execute_research_action_no_llm_service(self):
        execution_context = MagicMock(spec=ExecutionContext)
        execution_context.llm_service = None

        action = ResearchAction()
        result = await action.execute(execution_context, research_topic="AI")
        self.assertIn("error", result)

if __name__ == "__main__":
    unittest.main()
