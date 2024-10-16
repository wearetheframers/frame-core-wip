import unittest
from unittest.mock import MagicMock, patch
from frame.src.framer.framer import Framer
from frame.src.utils.config_parser import parse_json_config, parse_markdown_config


class TestFramerIO(unittest.TestCase):

    @patch("frame.src.framer.framer.load_from_file")
    def test_load_framer_from_file(self, mock_load):
        mock_load.return_value = MagicMock(spec=Framer)
        framer = Framer.load_from_file("dummy_path", MagicMock())
        self.assertIsInstance(framer, Framer)

    @patch("builtins.open", new_callable=unittest.mock.mock_open)
    @patch("json.dump")
    def test_export_to_json(self, mock_json_dump, mock_open):
        framer = Framer(
            config=MagicMock(),
            llm_service=MagicMock(),
            agency=MagicMock(),
            brain=MagicMock(),
            soul=MagicMock(),
            workflow_manager=MagicMock(),
        )
        framer.export_to_json("dummy_path")
        mock_open.assert_called_once_with("dummy_path", "w")
        mock_json_dump.assert_called_once()

    @patch("builtins.open", new_callable=unittest.mock.mock_open)
    @patch("frame.src.utils.config_parser.export_config_to_markdown")
    def test_export_to_markdown(self, mock_export, mock_open):
        framer = Framer(
            config=MagicMock(),
            llm_service=MagicMock(),
            agency=MagicMock(),
            brain=MagicMock(),
            soul=MagicMock(),
            workflow_manager=MagicMock(),
        )
        framer.export_to_markdown("dummy_path")
        mock_open.assert_called_once_with("dummy_path", "w")
        mock_export.assert_called_once_with(framer.config, "dummy_path")


if __name__ == "__main__":
    unittest.main()
