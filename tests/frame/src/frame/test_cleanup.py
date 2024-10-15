import pytest
from unittest.mock import patch, MagicMock
from frame.src.utils.cleanup import cleanup
from frame.src.utils.log_manager import setup_logging

# Configure logger for testing
setup_logging(testing=True)


def test_cleanup(capfd):
    cleanup()
    captured = capfd.readouterr()
    assert "Cleaning up Frame resources..." in captured.out


def test_cleanup_with_exception(capfd):
    with patch("frame.src.utils.cleanup.logger") as mock_logger:
        mock_logger.info.side_effect = Exception("Test exception")
        cleanup()
        captured = capfd.readouterr()
        assert "Error during cleanup logging: Test exception" in captured.out
        assert "Cleaning up Frame resources..." in captured.out


def test_cleanup_with_exception_and_capfd(capfd):
    with patch("frame.src.utils.cleanup.logger") as mock_logger:
        mock_logger.info.side_effect = Exception("Test exception")
        cleanup()
        captured = capfd.readouterr()
        assert "Error during cleanup logging: Test exception" in captured.err
        assert "Cleaning up Frame resources..." in captured.out
