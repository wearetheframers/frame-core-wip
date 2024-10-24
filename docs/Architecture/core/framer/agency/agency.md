---
title: Agency
weight: 30
---

# Agency Architecture

## Overview

The Agency component is responsible for roles, goals, and task management within a Framer. It manages the execution and state of tasks and workflows, and can automatically generate roles and goals when needed.

## Key Features

- Role and goal management, including automatic generation.
- Task creation and prioritization, including tasks generated from decisions.
- Workflow management.

## Automatic Role and Goal Generation

The Agency can automatically generate roles and goals for a Framer when they are not provided or are empty. The behavior is as follows:

- If both roles and goals are None, they will be generated using `generate_roles_and_goals()`.
- If roles is an empty list `[]`, no roles or goals will be assigned, as the Agency has no roles to base goals on.
- If goals is an empty list `[]` and roles is None, only goals will be generated.
- If both roles and goals are empty lists `[]`, no roles or goals will be assigned.
- If either roles or goals is provided (not None or empty list), the provided value will be used.

This ensures that Framers always have some roles and goals to guide their behavior, even if they are not explicitly defined by the user.

## Roles and Goals

Roles and goals in the Agency now have additional attributes:

- Roles have a priority level and a status (ACTIVE, INACTIVE, or SUSPENDED).
- Goals have a priority level and a status (ACTIVE, COMPLETED, or ABANDONED).

Multiple roles and goals can be active simultaneously, allowing for more complex and nuanced behavior of the Framer.

## Related Components

- [[brain]]: Handles decision-making processes for the Framer.
- [[soul]]: Manages memory and emotional states of a Framer.
- [[execution_context]]: Provides shared state and services for Framer actions.
