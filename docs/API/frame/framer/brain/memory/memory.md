# Memory

The Memory class manages memory storage and retrieval for Framers, integrating closely with perception processing and decision-making.

It supports both global and multi-user memory contexts, as well as different types of memory storage (core, short-term, and long-term). When no user ID is provided, memories are stored in a global context (DEFAULT_USER_ID). When multiple user IDs are provided, the memory retrieval process searches across all specified user IDs.

The memory system automatically determines whether to use memory retrieval based on the nature of the query:
- Questions containing personal pronouns ("my", "I", "we")
- Questions about personal preferences or past conversations 
- Questions requesting user-specific information

For general knowledge questions, the system will use direct responses without memory retrieval.

This is achieved using the MemoryService and Mem0Adapter, which abstract away the underlying storage solution and provide a flexible interface for memory operations. The architecture allows for easy swapping of memory components, offering alternatives like RAG with the same interface but different underlying drivers.

The `memory` service functions like a plugin but does not require explicit permissions to be accessed. It is always available to Framers, providing essential memory management capabilities. 

When `with-memory` is used, the Framer is also given permissions for `with-mem0-search-extract-summarize-plugin`. This ensures that the Framer can respond from memory effectively, leveraging the Mem0SearchExtractSummarizePlugin for comprehensive memory retrieval and response. This plugin might be refactored into a core component in the future to streamline its integration and usage.

## Memory Types

1. **Core Memory**: Essential, unchanging information about the Framer.
2. **Short-term Memory**: Recent perceptions and thoughts, limited to a certain number of items.
3. **Long-term Memory**: Persistent storage for important information and experiences.

## Integration with Perception

The Memory class works closely with the Brain's perception processing. When a new perception is processed, it can be added to short-term memory and, if deemed important, to long-term memory.

## Usage

To use the Memory class, instantiate it with the necessary configuration and use its methods to manage memory:

```python
memory = Memory(config)
memory.add_long_term_memory("Sample memory")
memory.add_short_term_memory({"type": "visual", "content": "A red apple"})
core_memory = memory.get_core_memory("identity")
```

## Related Components

- **MemoryService**: Provides the underlying memory operations.
- **Mem0Adapter**: Adapter for basic memory operations.
- **Brain**: Uses Memory for decision-making and perception processing.
- **Perception**: Represents sensory input that can be stored in memory.

## API Documentation

::: frame.src.framer.brain.memory.Memory
