---
title: Brain
weight: 25
---

# Brain Architecture

## Overview

The Brain component handles decision-making processes for the Framer, communicating with the Soul and Agency through the ExecutionContext.

## Key Features

- Perception processing: The Brain can process various types of incoming data (perceptions) such as text, images, and sounds, provided the appropriate plugins and inputs are available.
- Decision-making based on perceptions, goals, roles, context, and available actions.
- Interaction with language models through ExecutionContext.
- Memory storage and retrieval using ExecutionContext.
- Multi-modal perception processing.
- Execution of actions using ActionRegistry and ExecutionContext.
- Task and workflow creation based on decisions and context.
- Plugin integration: The Brain can use available plugins to extend its capabilities and perform a wider range of actions.
- Permission-based action execution: The Brain considers the Framer's permissions when deciding which actions to take.

## ExecutionContext

The Brain now uses an ExecutionContext, which provides:

- Centralized access to services (LLM, memory, EQ).
- Consistent interface for decision-making and action execution.
- Improved modularity and testability.

## Task Creation

The Brain component is responsible for processing perceptions and making decisions that lead to task creation. By analyzing the current state and context, the Brain determines the necessary actions and creates tasks to achieve the Framer's goals. These tasks are then executed using the ActionRegistry and ExecutionContext, ensuring a seamless workflow from perception to action.

## Key Methods

- `__init__(execution_context: ExecutionContext, ...)`: Initializes the Brain with an ExecutionContext.
- `process_perception(perception: Perception, ...)`: Processes perceptions and makes decisions, potentially leading to task creation.
- `make_decision(perception: Optional[Perception])`: Makes decisions based on current state and perception, which can result in task creation.
- `execute_decision(decision: Decision)`: Executes decisions using the ActionRegistry and ExecutionContext, facilitating task execution.

## Related Components

- [[soul]]: Manages memory and emotional states of a Framer.
- [[agency]]: Manages roles, goals, tasks, and workflows for the Framer.
- [[action_registry]]: Manages and executes actions using the ExecutionContext.
- [[execution_context]]: Provides necessary services for decision-making and action execution.
