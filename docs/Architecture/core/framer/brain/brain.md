---
title: Brain
weight: 25
---

# Brain Architecture

## Overview

The Brain component handles decision-making processes for the Framer, communicating with the Soul and Agency through the ExecutionContext.

## Key Features

- Decision-making based on goals and context.
- Interaction with language models through ExecutionContext.
- Memory storage and retrieval using ExecutionContext.
- Multi-modal perception processing.
- Execution of actions using ActionRegistry and ExecutionContext.

## ExecutionContext

The Brain now uses an ExecutionContext, which provides:

- Centralized access to services (LLM, memory, EQ).
- Consistent interface for decision-making and action execution.
- Improved modularity and testability.

## Key Methods

- `__init__(execution_context: ExecutionContext, ...)`: Initializes the Brain with an ExecutionContext.
- `process_perception(perception: Perception, ...)`: Processes perceptions and makes decisions.
- `make_decision(perception: Optional[Perception])`: Makes decisions based on current state and perception.
- `execute_decision(decision: Decision)`: Executes decisions using the ActionRegistry and ExecutionContext.

## Related Components

- [[soul]]: Manages memory and emotional states of a Framer.
- [[agency]]: Manages roles, goals, tasks, and workflows for the Framer.
- [[action_registry]]: Manages and executes actions using the ExecutionContext.
- [[execution_context]]: Provides necessary services for decision-making and action execution.
