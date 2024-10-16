import unittest
from unittest.mock import MagicMock, patch
from frame.src.framer.framer import Framer
from frame.src.utils.config_parser import load_framer_from_file, export_framer_to_json, export_framer_to_markdown

class TestFramerIO(unittest.TestCase):

    @patch('frame.src.utils.config_parser.load_framer_from_file')
    def test_load_framer_from_file(self, mock_load):
        mock_load.return_value = MagicMock()
        framer = load_framer_from_file('dummy_path')
        self.assertIsNotNone(framer)

    @patch('frame.src.utils.config_parser.export_framer_to_json')
    def test_export_framer_to_json(self, mock_export):
        framer = MagicMock(spec=Framer)
        export_framer_to_json(framer, 'dummy_path')
        mock_export.assert_called_once_with(framer, 'dummy_path')

    @patch('frame.src.utils.config_parser.export_framer_to_markdown')
    def test_export_framer_to_markdown(self, mock_export):
        framer = MagicMock(spec=Framer)
        export_framer_to_markdown(framer, 'dummy_path')
        mock_export.assert_called_once_with(framer, 'dummy_path')

if __name__ == '__main__':
    unittest.main()
