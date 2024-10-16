---
title: Action
weight: 50
---

# Action Architecture

## Overview

The Action component represents actionable items for Framers to work on. It includes a description of the action to be performed, a priority level, a status, and can store results and metadata.

## Key Features

- Action description and priority.
- Status and result management.
- Metadata storage.

## Task Creation

Task creation in the Framer architecture involves defining actionable items that the Framer can work on. Tasks are created based on decisions made by the Brain component, which processes perceptions and determines the necessary actions to achieve goals. The Action component stores details about the task, such as its description, priority, and status.

## Related Components

- [[decision]]: Represents a decision made by the Brain component of a Framer, which can lead to task creation.
- [[actionregistry]]: Manages and executes actions within the Frame framework, facilitating task management.
