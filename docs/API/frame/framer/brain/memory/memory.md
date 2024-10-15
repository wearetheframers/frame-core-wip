# Memory

The Memory class manages memory storage and retrieval for Framers.

It supports both global and multi-user memory contexts. When no user ID is provided,
memories are stored in a global context. When multiple user IDs are provided, the
memory retrieval process searches across all specified user IDs.

This is achieved using the MemoryService and Mem0Adapter, which abstract away the
underlying storage solution and provide a flexible interface for memory operations.

## Usage

To use the Memory class, instantiate it with the necessary configuration and use its methods to manage memory:

```python
memory = Memory(config)
memory.add_long_term_memory("Sample memory")
```

## Related Components

- **MemoryService**: Provides the underlying memory operations.
- **Mem0Adapter**: Adapter for basic memory operations.

## API Documentation

::: frame.src.framer.brain.memory.Memory