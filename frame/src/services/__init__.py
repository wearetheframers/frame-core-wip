from .llm.main import LLMService
from .context.local_context_service import LocalContext
from .context.shared_context_service import SharedContext
from .eq.main import EQService

# Create a function to get ExecutionContext to break circular imports
def get_execution_context():
    from .context.execution_context_service import ExecutionContext
    return ExecutionContext

# Create a function to get MemoryService to break circular imports
def get_memory_service():
    from .memory.main import MemoryService
    return MemoryService
