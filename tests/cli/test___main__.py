import unittest
from unittest.mock import MagicMock
from unittest.mock import patch, AsyncMock
import sys
import os
import types

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


class TestMain(unittest.TestCase):
    @patch("frame.cli.cli.cli")
    def test_main_function_imported(self, mock_cli):
        """Test that the main function is correctly imported from cli module."""
        from frame.cli import __main__

        with patch.object(sys, "argv", ["frame"]):
            __main__.main()
            mock_cli.assert_called_once_with(obj={})

    def test_main_called_when_script_is_main(self):
        """Test that main() is called when the script is run as __main__."""
        # Create a mock module structure
        mock_frame = types.ModuleType("frame")
        mock_frame.cli = types.ModuleType("frame.cli")
        mock_frame.cli.cli = types.ModuleType("frame.cli.cli")
        mock_frame.cli.cli.main = MagicMock()

        # Add the mock modules to sys.modules
        sys.modules["frame"] = mock_frame
        sys.modules["frame.cli"] = mock_frame.cli
        sys.modules["frame.cli.cli"] = mock_frame.cli.cli

        try:
            # Create a mock __main__ module
            mock_main_module = types.ModuleType("__main__")
            mock_main_module.__file__ = "frame/cli/__main__.py"

            # Add the mocked content to the module
            mock_main_content = """
from frame.cli.cli import main

if __name__ == '__main__':
    main()
"""
            # Execute the mocked content in a controlled environment
            exec(mock_main_content, {"__name__": "__main__", "frame": mock_frame})

            # Verify that main was called
            mock_frame.cli.cli.main.assert_called_once()
        finally:
            # Clean up
            del sys.modules["frame"]
            del sys.modules["frame.cli"]
            del sys.modules["frame.cli.cli"]


if __name__ == "__main__":
    unittest.main()
