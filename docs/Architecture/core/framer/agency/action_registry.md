---
title: ActionRegistry
weight: 55
---

# ActionRegistry Architecture

## Overview

The ActionRegistry component is responsible for managing and executing actions within the Frame framework. It allows for the registration, retrieval, and execution of actions.

## Key Features

- Action registration and retrieval.
- Action execution management using ExecutionContext.
- Default actions and customization.

## ExecutionContext

The ActionRegistry now uses an ExecutionContext, which provides:

- Consistent access to services (LLM, memory, EQ) across all actions.
- Improved modularity and testability.
- Simplified action implementation by providing necessary resources.

## Key Methods

- `__init__(execution_context: ExecutionContext)`: Initializes the ActionRegistry with an ExecutionContext.
- `register_action(action_name: str, action_func: Callable, ...)`: Registers a new action.
- `execute_action(action_name: str, parameters: dict)`: Executes an action using the ExecutionContext.

## Related Components

- [[action]]: Represents actionable items for Framers to work on.
- [[brain]]: Handles decision-making processes for the Framer.
- [[execution_context_service]]: Provides necessary services and shared state for action execution.
