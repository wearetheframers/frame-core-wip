import asyncio
from unittest import IsolatedAsyncioTestCase, mock
from unittest.mock import MagicMock, patch, AsyncMock
from frame.src.framer.framer import Framer
from frame.src.services.llm.main import LLMService
from frame.src.utils.config_parser import parse_json_config, parse_markdown_config
from frame.src.framer.framer_factory import FramerFactory


class TestFramerIO(IsolatedAsyncioTestCase):

    @patch("frame.src.framer.framer.Framer.load_from_file")
    async def test_load_framer_from_file(self, mock_load):
        mock_load.return_value = AsyncMock(spec=Framer)
        framer_factory = FramerFactory(MagicMock(), MagicMock(spec=LLMService))
        framer = await framer_factory.create_framer(
            memory_service=None,
            eq_service=None,
        )
        self.assertIsInstance(framer, Framer)

    @patch(
        "frame.src.framer.framer.Framer._generate_initial_roles_and_goals",
        new_callable=AsyncMock,
    )
    @patch("json.dump")
    @patch(
        "frame.src.utils.config_parser.export_config_to_json", new_callable=AsyncMock
    )
    @patch("builtins.open", new_callable=mock.mock_open)
    @patch(
        "frame.src.services.llm.main.LLMService.get_completion", new_callable=AsyncMock
    )
    async def test_export_to_json(
        self,
        mock_get_completion,
        mock_open,
        mock_json_dump,
        mock_export_config,
        mock_generate_roles,
    ):
        mock_get_completion.return_value = (
            '{"roles": [], "goals": []}'  # Return a valid JSON string
        )
        agency_mock = AsyncMock()
        agency_mock.roles = []
        agency_mock.goals = []
        framer = Framer(
            config=MagicMock(),
            llm_service=MagicMock(),
            agency=agency_mock,
            brain=MagicMock(),
            soul=MagicMock(),
            workflow_manager=MagicMock(),
        )
        await framer.export_to_file("dummy_path")
        mock_open.assert_called_once_with("dummy_path", "w")
        mock_export_config.assert_called_once_with(framer.config.to_dict(), mock_open(), indent=4)
        mock_export_config.assert_called_once_with(
            framer.config.to_dict(), mock_open(), indent=4
        )
        mock_json_dump.assert_called_once()

    @patch(
        "frame.src.framer.framer.Framer._generate_initial_roles_and_goals",
        new_callable=AsyncMock,
    )
    @patch("builtins.open", new_callable=mock.mock_open)
    @patch("frame.src.utils.config_parser.export_config_to_markdown")
    async def test_export_to_markdown(
        self, mock_export_config, mock_open, mock_generate_roles
    ):
        framer = Framer(
            config=MagicMock(),
            llm_service=MagicMock(),
            agency=MagicMock(),
            brain=MagicMock(),
            soul=MagicMock(),
            workflow_manager=MagicMock(),
        )
        await framer.export_to_markdown("dummy_path")
        mock_open.assert_called_once_with("dummy_path", "w")
        mock_export_config.assert_called_once_with(framer.config, mock_open())


if __name__ == "__main__":
    import unittest

    unittest.main()
