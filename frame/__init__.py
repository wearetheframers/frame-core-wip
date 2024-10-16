"""
Frame: A multi-modal cognitive agent framework.
"""

from .src.utils.log_manager import setup_logging
from .frame import Frame  # Direct import of Frame class
from .src.utils.cleanup import cleanup

# Configure logging
logger = setup_logging()

__version__ = "0.1.0"


from .src.utils.helpers import lazy_import as __lazy_import


def __getattr__(name):
    if name == "cli":
        return __lazy_import("cli.cli").cli
    elif name == "main":
        return __lazy_import("cli.cli").main
    elif name in (
        "Framer",
        "FramerFactory",
        "Agency",
        "Mind",
        "Perception",
        "Soul",
        "SharedContext",
        "Memory",
        "Task",
        "TaskStatus",
        "LLMService",
        "DSPyAdapter",
        "HuggingFaceAdapter",
        "LMQLAdapter",
        "Mem0Adapter",
        "Decision",
        "EQService",
    ):
        return getattr(__lazy_import("src"), name)
    elif name == "sync_frame":
        return __lazy_import("sync_frame").sync_frame
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


logger.info(f"Frame v{__version__} initialized")


import atexit

atexit.register(cleanup)

# Ensure all handlers are closed properly
import logging


from .src.utils.helpers import close_logger_handlers as __close_logger_handlers


atexit.register(lambda: __close_logger_handlers())

# Expose the CLI for easy access
from .cli.cli import cli, main
from frame.frame import Frame
from frame.src.framer.config import FramerConfig
from frame.src.framer.agency.agency import Agency
from frame.src.framer.brain.brain import Brain
from frame.src.framer.soul.soul import Soul
from frame.src.framer.agency.tasks.workflow.workflow_manager import WorkflowManager
from frame.src.framer.agency.tasks.task import Task
from frame.src.services.llm.main import LLMService
from frame.src.framer.brain.perception import Perception
from frame.src.framer.brain.decision import Decision
from frame.src.framer.framer_factory import FramerBuilder
from frame.src.framed.framed_factory import FramedBuilder
from frame.src.services.memory.main import MemoryService
from frame.src.services.eq.main import EQService

# Expose the main classes and functions

# Version information
__version__ = "0.1.0"
