import logging
import os
import time
from datetime import datetime, timedelta
from frame.src.utils.log_manager import (
    setup_logging,
    get_logger,
    close_logging,
    cleanup_old_logs,
)


def test_setup_logging():
    logger = setup_logging()
    assert isinstance(logger, logging.Logger)
    assert logger.name == "frame"
    assert logger.level == logging.INFO

    # Check for NullHandler
    assert any(isinstance(handler, logging.NullHandler) for handler in logger.handlers)

    # Check for FileHandler and StreamHandler
    handlers = [h for h in logger.handlers if not isinstance(h, logging.NullHandler)]
    assert len(handlers) == 2
    assert any(isinstance(handler, logging.FileHandler) for handler in handlers)
    assert any(isinstance(handler, logging.StreamHandler) for handler in handlers)

    # Clean up
    for handler in logger.handlers:
        logger.removeHandler(handler)
        if isinstance(handler, logging.FileHandler):
            handler.close()
            if os.path.exists(handler.baseFilename):
                os.remove(handler.baseFilename)


def test_get_logger():
    logger = get_logger("test_logger")
    assert isinstance(logger, logging.Logger)
    assert logger.name == "test_logger"


def test_close_logging():
    logger = setup_logging()
    close_logging(logger)
    assert len(logger.handlers) == 0


def test_cleanup_old_logs(tmp_path):
    # Create some dummy log files
    log_dir = tmp_path / "logs"
    log_dir.mkdir()

    # Create an old log file (9 days ago)
    old_date = (datetime.now() - timedelta(days=9)).strftime("%Y-%m-%d")
    (log_dir / f"framer_{old_date}.log").touch()

    # Create a new log file (today)
    new_date = datetime.now().strftime("%Y-%m-%d")
    (log_dir / f"framer_{new_date}.log").touch()

    cleanup_old_logs(str(log_dir))

    assert not (log_dir / f"framer_{old_date}.log").exists()
    assert (log_dir / f"framer_{new_date}.log").exists()
