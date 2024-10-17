# Framer

::: frame.src.framer.Framer
    options:
      halt:
        description: "Stops the Framer from acting and processing new tasks."
      show_root_heading: false
      show_source: false
# Framer

::: frame.src.framer.framer.Framer
    options:
      show_root_heading: false
      show_source: false

## Overview

The `Framer` class represents an AI agent with cognitive capabilities. It integrates various components such as agency, brain, soul, and workflow management to create a comprehensive AI entity capable of processing perceptions, making decisions, and executing tasks.

## Key Components

### Agency

Manages roles, goals, and tasks for the Framer. 
- Roles are active by default when created, and multiple roles can be active simultaneously.
- Goals have different statuses (ACTIVE, COMPLETED, ABANDONED) which influence the Framer's decision-making process. Multiple goals can be active at the same time.

### Brain

Handles decision-making processes, integrating perceptions, memories, and thoughts. It considers the status of goals and active roles when processing perceptions and making decisions.

### Soul

Represents the core essence and personality of a Framer.

### WorkflowManager

Manages workflows and tasks.

## Key Methods

### `sense`

Processes a perception and makes a decision based on current goals, their statuses, and active roles.

### `prompt`

Processes a text prompt as a new perception.

### `perform_task`

Executes a specific task.

### `generate_tasks_from_perception`

Generates tasks based on a given perception, considering current goals, their statuses, and active roles.

## Usage

The Framer processes perceptions and makes decisions based on its current goals, active roles, and the status of each goal:

```python
framer = await Framer.create(config, llm_service)

# Process a perception
decision = await framer.sense(perception)

# Process a text prompt
decision = await framer.prompt("What is the current status of our efficiency goal?")

# Perform a task
result = await framer.perform_task(task)
```

The Framer's decision-making process takes into account the status of each goal (ACTIVE, COMPLETED, ABANDONED) and the currently active roles, prioritizing actions that align with active goals and roles, and adapting its behavior as goals are completed or abandoned.
