# Workflow and WorkflowManager

## Workflow

A Workflow is a sequence of related tasks that need to be completed to achieve a specific goal. It manages the execution and state of its tasks, and provides methods for adding, retrieving, and completing tasks.

Attributes:
- **id** (str): The unique identifier for the workflow.
- **name** (str): The name of the workflow.


## Related Components

- **Task**: Represents an actionable item within a workflow.
- **WorkflowManager**: Manages multiple workflows and their execution.


## Usage

To use the Workflow class, create an instance and manage tasks through its methods:

```python
workflow = Workflow(id="workflow1", name="Sample Workflow")
workflow.add_task(task)
```

## API Documentation

::: frame.src.framer.agency.tasks.workflow.Workflow
