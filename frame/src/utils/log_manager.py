import logging
from typing import Optional
import os
import datetime
import glob
import sys
import re
from colorama import init, Fore, Style  # Import colorama for colored logging

# Initialize colorama
init(autoreset=True)


def setup_logging(level: Optional[int] = None, testing: bool = False) -> logging.Logger:
    """
    Set up and configure logging for the application.

    Args:
        level (Optional[int]): The logging level to set. If None, defaults to INFO.
        testing (bool): If True, configure logging for testing environment.

    Returns:
        logging.Logger: The configured logger instance.
    """
    logger = logging.getLogger("frame")
    logger.propagate = False
    if level is None:
        level = logging.INFO
    logger.setLevel(level)

    # Remove all existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Add a NullHandler to prevent "No handlers could be found" warnings
    logger.addHandler(logging.NullHandler())

    if not testing:
        # Create file handler and set level
        frame_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        log_dir = os.path.join(frame_dir, "logs")
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(
            log_dir, f"framer_{datetime.datetime.now().strftime('%Y-%m-%d')}.log"
        )
        fh = logging.FileHandler(log_file, mode="a")  # 'a' for append mode
        fh.setLevel(level)

        # Create console handler and set level
        ch = logging.StreamHandler(sys.stdout)  # Use sys.stdout instead of sys.stderr
        ch.setLevel(level)

        # Create formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        # Define a custom formatter function for console output
        class ColorFormatter(logging.Formatter):
            def format(self, record):
                log_colors = {
                    "DEBUG": Fore.WHITE,
                    "INFO": Fore.GREEN,
                    "WARNING": Fore.YELLOW,
                    "ERROR": Fore.RED,
                    "CRITICAL": Fore.RED + Style.BRIGHT,
                }
                levelname_color = log_colors.get(record.levelname, Fore.WHITE)
                record.asctime = f"{Fore.CYAN}{record.asctime}{Style.RESET_ALL}"
                record.name = f"{Fore.BLUE}{record.name}{Style.RESET_ALL}"
                record.levelname = (
                    f"{levelname_color}{record.levelname}{Style.RESET_ALL}"
                )
                record.message = f"{Style.BRIGHT}{record.getMessage()}{Style.RESET_ALL}"
                return super().format(record)

        # Add formatter to handlers
        fh.setFormatter(formatter)  # Use standard formatter for file handler
        ch.setFormatter(
            ColorFormatter(fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )  # Use colored formatter for console

        # Add handlers to logger
        logger.addHandler(fh)
        logger.addHandler(ch)

        logger.info("Logging initialized")

        cleanup_old_logs(log_dir)

    return logger


def add_stream_handler(logger: logging.Logger, level: Optional[int] = None) -> None:
    """
    Add a StreamHandler to the logger for testing purposes.

    Args:
        logger (logging.Logger): The logger to add the handler to.
        level (Optional[int]): The logging level for the handler. If None, uses the logger's level.
    """
    if level is None:
        level = logger.level

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(level)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    ch.setFormatter(formatter)
    logger.addHandler(ch)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the specified name.

    Args:
        name (str): The name of the logger.

    Returns:
        logging.Logger: The logger instance.
    """
    return logging.getLogger(name)


def close_logging(logger: logging.Logger) -> None:
    """
    Close all handlers associated with the logger.

    Args:
        logger (logging.Logger): The logger instance to close handlers for.
    """
    handlers = logger.handlers[:]
    for handler in handlers:
        handler.close()
        logger.removeHandler(handler)


def cleanup_old_logs(log_dir: str, days: int = 7) -> None:
    """
    Clean up log files older than the specified number of days.

    Args:
        log_dir (str): Directory containing the log files.
        days (int): Number of days to keep logs for. Defaults to 7.
    """
    current_date = datetime.datetime.now().date()
    for log_file in glob.glob(os.path.join(log_dir, "framer_*.log")):
        match = re.search(
            r"framer_(\d{4}-\d{2}-\d{2})\.log", os.path.basename(log_file)
        )
        if match:
            file_date = datetime.datetime.strptime(match.group(1), "%Y-%m-%d").date()
            if (current_date - file_date).days > days:
                os.remove(log_file)
                print(f"Removed old log file: {log_file}")
