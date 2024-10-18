---
title: Frame
weight: 10
---

# Frame Architecture

## Overview

The Frame component serves as the main interface for creating and managing Framer instances. It acts as the central hub for initializing and orchestrating the various components of the framework.

## Key Responsibilities

- Initializing the framework with various API keys and configurations.
- Creating individual Framers with specific roles and goals.
- Managing LLM services and model interactions. Note: DSPy does not support streaming mode.
- Creating Framed groups for multi-agent coordination.
- Supporting a plugin system for extending functionality, including a marketplace for premium and community plugins.

## Related Components

- [[framer]]: Represents an individual AI agent with capabilities for task management, decision-making, and interaction with language models. It now includes an ExecutionContextService for improved modularity and consistency across actions.
- [[framed]]: A collection of Framer objects working together to achieve complex tasks.
