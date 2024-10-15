---
title: Mem0 Adapter
publish: true
---

# Mem0 Adapter

## Overview

The Mem0Adapter class is responsible for interfacing with the Mem0 memory system. It provides methods to store, retrieve, and manage memory data.

## Key Features

- **Memory Storage**: Store memory entries in the Mem0 system.
- **Memory Retrieval**: Retrieve memory entries from the Mem0 system.
- **Memory Management**: Manage memory entries, including deletion.

## Usage

To use the Mem0Adapter class, initialize it with the necessary configuration:

```python
from frame.src.framer.brain.memory.memory_adapters.mem0.mem0_adapter import Mem0Adapter

config = {"setting1": "value1", "setting2": "value2"}
adapter = Mem0Adapter(config=config)

adapter.store_memory(key="example_key", value="example_value")
memory_value = adapter.retrieve_memory(key="example_key")
adapter.delete_memory(key="example_key")
```

## API Documentation

::: frame.src.framer.brain.memory.memory_adapters.mem0.mem0_adapter.Mem0Adapter
