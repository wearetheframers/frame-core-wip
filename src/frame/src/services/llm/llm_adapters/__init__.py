from .lmql import LMQLAdapter
from .dspy import DSPyAdapter

# Dynamic adapter imports will be handled by plugin system
available_adapters = {
    'lmql': LMQLAdapter,
    'dspy': DSPyAdapter
}

def register_adapter(name: str, adapter_class):
    """Register a new LLM adapter dynamically"""
    available_adapters[name] = adapter_class
