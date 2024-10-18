from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .context.local_context_service import LocalContext
    from .context.shared_context_service import SharedContext
    from .context.execution_context_service import ExecutionContext
    from .memory.main import MemoryService

def get_local_context() -> 'LocalContext':
    from .context.local_context_service import LocalContext
    return LocalContext()

def get_shared_context() -> 'SharedContext':
    from .context.shared_context_service import SharedContext
    return SharedContext()

def get_execution_context() -> 'ExecutionContext':
    from .context.execution_context_service import ExecutionContext
    return ExecutionContext()

def get_memory_service() -> 'MemoryService':
    from .memory.main import MemoryService
    return MemoryService()
