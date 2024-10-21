"""
Shared Context Service Module

This module provides the SharedContextService class, which extends the
ContextService to manage shared roles and goals across multiple Framers.
"""

from .execution_context_service import ExecutionContext


class SharedContext(ExecutionContext):
    pass
