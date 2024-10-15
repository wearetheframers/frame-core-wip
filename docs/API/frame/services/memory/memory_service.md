---
title: Memory Service
publish: true
---

# Memory Service

## Overview

The Memory Service is designed to manage memory storage and retrieval for Framers. It supports both global and multi-user memory contexts, providing a flexible interface for memory operations. This service is essential for maintaining state and context across different tasks and interactions.

## Key Components

- **core**: Core memory storage for essential data.
- **short_term**: Short-term memory storage for temporary data.
- **long_term_memory**: Long-term memory storage for persistent data.

## Memory Adapters

The Memory Service uses adapters to interact with different storage solutions. These adapters provide a flexible interface for memory operations, abstracting away the underlying storage details.

### Available Adapters

- **Mem0Adapter**: Adapter for basic memory operations.

## How It Works

The Memory Service uses adapters to interact with different storage solutions. It provides methods to add, retrieve, and search memories, ensuring that Framers can access relevant information when needed. The service also supports memory updates and history tracking.

## Usage

To use the Memory Service, initialize it with the desired configuration and use its methods to manage memory operations. The service abstracts the underlying storage details, allowing for seamless memory management.

## API Documentation

::: frame.src.services.memory.main.MemoryService
