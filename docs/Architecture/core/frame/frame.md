---
title: Frame Architecture
weight: 10
---

# Frame Architecture

## Overview

The Frame component serves as the main interface for creating and managing Framer instances. It acts as the central hub for initializing and orchestrating the various components of the framework, providing a robust foundation for building advanced AI agents capable of multi-modal perception processing and collaborative work.

## Key Responsibilities

- Initializing the framework with various API keys and configurations.
- Creating individual Framers with specific roles, goals, and permissions.
- Managing LLM services and model interactions, including support for local models.
- Creating Framed groups for multi-agent coordination and collaborative problem-solving.
- Supporting an extensive plugin system for extending functionality, including a marketplace for premium and community plugins.
- Handling multi-modal perceptions and integrating them into the decision-making process.
- Managing layered memory systems for improved context understanding and entity relationships.

## Related Components

### Custom Action Registry

In the autonomous vehicle example, we demonstrate how to replace the default action registry with a custom one. This allows for a more flexible and hackable system where you can replace or extend default behaviors. The `process_perception` function takes precedence over the observe action, showing how you can customize the action registry. You can also remove actions from the Framer behavior in plugins programmatically.

Frame includes several default plugins and services that are automatically available to Framers. These include:

- **Services**: `memory`, `eq`, and `shared_context` are special plugins called services. They function like plugins but do not require explicit permissions to be accessed. They are always available to Framers, enhancing their capabilities by providing essential functionalities without the need for additional permissions.

- **Default Plugin**: The `Mem0SearchExtractSummarizePlugin` is included as a default plugin. It provides a response mechanism that requires memory retrieval, functioning as a Retrieval-Augmented Generation (RAG) mechanism. By default, all Framers inherit this action, enabling them to search, extract, and summarize information effectively.

- [[framer]]: Represents an individual AI agent with capabilities for task management, decision-making, and interaction with language models. It now includes an ExecutionContextService for improved modularity and consistency across actions.
- [[framed]]: A collection of Framer objects working together to achieve complex tasks.
