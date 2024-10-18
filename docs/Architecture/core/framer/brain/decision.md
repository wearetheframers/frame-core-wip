---
title: Decision
weight: 45
---

# Decision Architecture

## Overview

The Decision component represents a decision made by the Brain component of a Framer. It includes an action, parameters, reasoning, confidence, priority, and expected results.

## Key Features

- **Perception Processing**: Decisions are made based on incoming perceptions, which can be any type of data (text, images, sounds) that the Framer can process.
- **Context-Aware Decision Making**: Decisions take into account the Framer's current roles, goals, and available actions.
- **Priority Management**: Actions can be prioritized to influence decision-making, ensuring that more critical actions are preferred.
- **Plugin Integration**: Decisions can involve actions provided by plugins, extending the Framer's capabilities.
- **Permission-Based Decision Making**: The Framer's permissions are considered when making decisions, ensuring it only chooses actions it's allowed to perform.
- Action representation.
- Decision parameters and reasoning.
- Confidence and priority management.

## Task Creation

The Decision component plays a crucial role in task creation by evaluating perceptions and determining the appropriate actions. Once a decision is made, it can result in the creation of tasks that are then managed by the Action component. This process ensures that the Framer can effectively respond to its environment and achieve its objectives.

## Related Components

- [[brain]]: Handles decision-making processes for the Framer, which can lead to task creation.
- [[action]]: Represents actionable items for Framers to work on, created as a result of decisions.
