"""
Shared Context Service Module

This module provides the SharedContextService class, which extends the
ContextService to manage shared roles and goals across multiple Framers.
"""

from .execution_context_service import ExecutionContext


class SharedContext(ExecutionContext):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.shared_state = kwargs
        self.llm_service = kwargs.get('llm_service', None)
