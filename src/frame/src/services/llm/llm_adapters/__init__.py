"""
LLM Adapters for Frame

Core adapter:
- LMQL: Default adapter that provides the base LLM interface

Optional plugin adapters (require explicit permissions):
- DSPy: Advanced prompt programming (with_dspy)
- HuggingFace: Local model support (with_huggingface)
"""

from .lmql import LMQLAdapter
from .dspy import DSPyAdapter
from .huggingface import HuggingFaceAdapter

__all__ = ['LMQLAdapter', 'DSPyAdapter', 'HuggingFaceAdapter']

# LMQL is the core adapter, always available
available_adapters = {
    'lmql': LMQLAdapter,
    'dspy': DSPyAdapter,
    'huggingface': HuggingFaceAdapter
}

def register_adapter(name: str, adapter_class):
    """
    Register a new LLM adapter dynamically
    
    Plugin adapters should use this to register themselves when loaded.
    Requires appropriate permissions (e.g., with_dspy, with_huggingface)
    """
    available_adapters[name] = adapter_class
    if adapter_class.__name__ not in __all__:
        __all__.append(adapter_class.__name__)
