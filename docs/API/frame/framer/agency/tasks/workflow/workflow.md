# Workflow and WorkflowManager

## Workflow

A Workflow is a sequence of related tasks that need to be completed to achieve a specific goal. It manages the execution and state of its tasks, and provides methods for adding, retrieving, and completing tasks.

Attributes:
- **id** (str): The unique identifier for the workflow.
- **name** (str): The name of the workflow.


## Related Components

- **Task**: Represents an actionable item within a workflow. Tasks use the same priority system as roles and goals, allowing for consistent prioritization across the Framer.
- **WorkflowManager**: Manages multiple workflows and their execution, taking into account the priorities of tasks within each workflow.

## Priority System

Workflows leverage the priority system of their constituent tasks. When executing a workflow, the WorkflowManager considers the priorities of individual tasks to determine the order of execution. This ensures that high-priority tasks within a workflow are addressed before lower-priority ones, even if they were added to the workflow later.


## Usage

To use the Workflow class, create an instance and manage tasks through its methods:

```python
workflow = Workflow(id="workflow1", name="Sample Workflow")
workflow.add_task(task)
```

## API Documentation

::: frame.src.framer.agency.tasks.workflow.Workflow
