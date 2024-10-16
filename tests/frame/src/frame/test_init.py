import sys
import pytest
import logging
from unittest.mock import patch, MagicMock
from frame.src.utils.cleanup import cleanup, close_logger_handlers
from frame.src.utils.log_manager import get_logger
from io import StringIO
from frame.src.framer.soul.soul import Soul
from frame.src.framed.config import FramedConfig
from frame.src.services.llm.main import LLMService
from frame.src.framer.agency import Agency
from frame.src.framer.brain import Brain
from frame.src.framer.soul import Soul
from frame.src.framer.agency.execution_context import ExecutionContext

logger = get_logger(__name__)


@pytest.fixture(autouse=True)
def setup_logger():
    # Set the logger to DEBUG level
    logger.setLevel(logging.DEBUG)
    # Add a StringIO handler for testing
    string_io = StringIO()
    handler = logging.StreamHandler(string_io)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(levelname)s: %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    yield string_io
    # Clean up after the test
    logger.handlers.clear()
    logger.setLevel(logging.INFO)  # Reset to default level


@pytest.fixture
def sample_soul():
    return Soul(seed={"text": "You are a helpful assistant."})


def test_cleanup(setup_logger):
    cleanup(logger)
    log_output = setup_logger.getvalue()

    # Check logs
    assert (
        "Cleaning up Frame resources..." in log_output
    ), f"Cleanup message not found in: {log_output}"


def test_cleanup_with_logger():
    with patch("frame.src.utils.cleanup.get_logger") as mock_get_logger:
        mock_logger = mock_get_logger.return_value
        mock_logger = mock_get_logger.return_value
        cleanup(mock_logger)
        mock_logger.info.assert_called_once_with("Cleaning up Frame resources...")


def test_cleanup_with_print():
    with patch("builtins.print") as mock_print:
        cleanup()
        mock_print.assert_called_with("Cleaning up Frame resources...", flush=True)


def test_cleanup_with_exception():
    with patch(
        "frame.src.utils.log_manager.get_logger", return_value=MagicMock()
    ) as mock_get_logger:
        mock_logger = mock_get_logger.return_value
        mock_logger.info.side_effect = Exception("Test exception")
        with patch("builtins.print") as mock_print:
            cleanup(mock_logger)
            mock_print.assert_any_call(
                "Error during cleanup logging: Test exception",
                file=sys.stderr,
                flush=True,
            )
            mock_print.assert_any_call("Cleaning up Frame resources...", flush=True)


@pytest.mark.asyncio
async def test_framed_initialization():
    config = FramedConfig(name="TestFramed")
    llm_service = LLMService()
    agency = Agency(llm_service=llm_service, context={})
    brain = Brain(llm_service=llm_service, roles=[], goals=[])
    soul = Soul(seed={})


def test_cleanup_with_exception_and_capfd(capfd):
    with patch(
        "frame.src.utils.log_manager.get_logger", return_value=MagicMock()
    ) as mock_get_logger:
        mock_logger = mock_get_logger.return_value
        mock_logger.info.side_effect = Exception("Test exception")
        cleanup(mock_logger)
        captured = capfd.readouterr()
        assert "Error during cleanup logging: Test exception" in captured.err
        assert "Cleaning up Frame resources..." in captured.out
