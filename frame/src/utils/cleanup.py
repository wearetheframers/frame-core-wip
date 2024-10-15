import logging
import atexit
import sys
from frame.src.utils.log_manager import get_logger

logger = get_logger(__name__)


def close_logger_handlers(logger=None):
    """Close all handlers for the given logger."""
    if logger is None:
        logger = logging.getLogger()
    for handler in logger.handlers[:]:
        try:
            handler.close()
        except Exception:
            pass  # Ignore errors when closing handlers
        logger.removeHandler(handler)


def cleanup(logger=None):
    """Perform cleanup operations."""
    if logger is None:
        logger = get_logger(__name__)

    # Register the close_logger_handlers function to be called at exit
    atexit.register(close_logger_handlers, logger)

    # Unregister any previous close_logger_handlers functions
    if hasattr(atexit, "_exithandlers"):
        atexit._exithandlers = [
            (func, args, kwargs)
            for func, args, kwargs in atexit._exithandlers
            if not (
                func.__name__ == "close_logger_handlers"
                and func != close_logger_handlers
            )
        ]

    message = "Cleaning up Frame resources..."
    try:
        print(message, flush=True)
        logger.info(message)
    except Exception as e:
        error_message = f"Error during cleanup logging: {e}"
        print(error_message, file=sys.stderr, flush=True)

    close_logger_handlers(logger)
