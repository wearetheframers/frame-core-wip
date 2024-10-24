---
title: Decision
weight: 45
---

# Decision Architecture

## Overview

The Decision component represents a decision made by the Brain component of a Framer. It includes an action, parameters, reasoning, confidence, priority, and expected results.

## Key Features

- **Perception Processing**: Decisions are made based on incoming perceptions, which can be any type of data (text, images, sounds) that the Framer can process. Framers automatically process perceptions as they are received.
- **Context-Aware Decision Making**: Decisions take into account the Framer's current roles, goals, and available actions.
- **Priority Management**: Actions can be prioritized to influence decision-making, ensuring that more critical actions are preferred.
- **Plugin Integration**: Decisions can involve actions provided by plugins, extending the Framer's capabilities through the Brain's action registry.
- **Permission-Based Decision Making**: The Framer's permissions are considered when making decisions, ensuring it only chooses actions it's allowed to perform.
- **Execution Modes**: Decisions can be executed automatically, require user approval, or be deferred for later execution.
- **Task Creation**: Decisions can lead to the creation of tasks within the Agency's task management system.

## Parameter Validation

The Decision component now performs validation of action parameters. When a decision is made, the parameters associated with the chosen action are checked to ensure they meet the expected format and contain all required fields. If invalid parameters are detected, the decision can be adjusted or flagged for correction, preventing execution errors and enhancing system robustness.

## Decision Execution in Framer

In the Framer architecture, decisions are central to the operation of the AI agent. A decision is a structured plan of action that the agent intends to execute based on its current perception and context. However, there are scenarios where a decision might not be executed immediately, leading to another decision being made. These scenarios include:

1. **Decision Already Executed**: If a decision has already been executed, the system will skip re-execution to prevent redundant actions. This is typically logged with a message like "Decision already executed, skipping re-execution."

2. **Framer Not Ready**: If the Framer is not in a state to execute decisions (e.g., during initialization or when certain dependencies are not yet loaded), the decision will be queued for later execution.

3. **Invalid Decision**: If the decision is deemed invalid due to missing or incorrect parameters, it may be discarded, prompting the system to make a new decision.

4. **Priority Override**: In some cases, a new perception or context change might lead to a higher-priority decision overriding the current one, causing the system to pivot to the new decision.

## Related Components

- [[brain]]: Handles decision-making processes for the Framer, which can lead to task creation.
- [[action]]: Represents actionable items for Framers to work on, created as a result of decisions.
