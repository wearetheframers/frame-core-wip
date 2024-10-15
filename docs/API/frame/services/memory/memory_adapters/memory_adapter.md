# Memory Adapter

The Memory Adapter module provides an interface for managing memory storage and retrieval in the Frame system. It supports both global and multi-user memory contexts, allowing Framers to store and access information across different sessions and users.

## Features

- **Global Memory**: Allows Framers to store and retrieve information that is accessible across all sessions and users.
- **Multi-User Memory**: Supports user-specific memory contexts, enabling personalized interactions and experiences.
- **Memory Persistence**: Ensures that important information is retained across sessions and can be accessed when needed.

## Usage

To use the Memory Adapter, instantiate the adapter class and call its methods to store and retrieve information.

```python
from services.memory.memory_adapter import MemoryAdapter

memory_adapter = MemoryAdapter()
memory_adapter.store("user123", "favorite_color", "blue")
color = memory_adapter.retrieve("user123", "favorite_color")
print(color)  # Output: blue
```

## Configuration

The Memory Adapter can be configured to use different storage backends, such as in-memory storage, databases, or external services, depending on the application's requirements.

## Extensibility

The Memory Adapter is designed to be extensible, allowing developers to implement custom storage backends or integrate with existing memory management systems.
