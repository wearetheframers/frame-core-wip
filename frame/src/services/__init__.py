from .llm.main import LLMService
from .eq.main import EQService

# Create functions to get services to break circular imports
def get_local_context():
    from .context.local_context_service import LocalContext
    return LocalContext

def get_shared_context():
    from .context.shared_context_service import SharedContext
    return SharedContext

def get_execution_context():
    from .context.execution_context_service import ExecutionContext
    return ExecutionContext

def get_memory_service():
    from .memory.main import MemoryService
    return MemoryService
