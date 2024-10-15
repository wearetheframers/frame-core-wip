import importlib
import logging


def lazy_import(name):
    """
    Lazily import a module by name.

    Args:
        name (str): The name of the module to import.

    Returns:
        module: The imported module.
    """
    return importlib.import_module(name)


def close_logger_handlers(logger):
    """
    Close all handlers associated with a logger.

    Args:
        logger (logging.Logger): The logger whose handlers should be closed.
    """
    for handler in logger.handlers:
        handler.close()
    logging.shutdown()
