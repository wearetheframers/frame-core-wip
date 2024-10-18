from .memory.main import MemoryService
from .llm.main import LLMService
from .context.local_context_service import LocalContext
from .context.shared_context_service import SharedContext
from .eq.main import EQService

# Create a function to get ExecutionContext to break circular imports
def get_execution_context():
    from .context.execution_context_service import ExecutionContext
    return ExecutionContext
