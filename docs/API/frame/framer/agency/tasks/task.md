# Task Package

The Task package is a part of the [[frame|Frame-Core]] system and is responsible for representing and managing tasks within the system.

## Usage

To create and manage a task within the [[frame|Frame-Core]] system, you can follow this example:

```python
from frame.src.framer.agency.tasks.task import Task

# Create a new task
task = Task(
    description="Analyze market trends",
    priority=8,  # Priority ranges from 1 to 10, with 10 being the highest
    status="pending",
    results=None,
    metadata={"assigned_to": "analyst_team"}
)

# Convert the task to a dictionary
task_dict = task.to_dict()
print(task_dict)

# Update task status
task.status = "in_progress"

# Access task attributes
print(f"Task Description: {task.description}")
print(f"Task Priority: {task.priority}")
print(f"Task Status: {task.status}")
```

## Related Components

- [[agency]]: Manages roles, goals, tasks, and workflows for [[framer|Framers]].
- [[workflow]]: Represents a sequence of related tasks to achieve a specific goal.
- [[roles]]: Defines roles with priorities that influence task execution.
- [[goals]]: Defines goals with priorities that guide task creation and execution.

## API Documentation

::: frame.src.framer.agency.tasks.task.Task

## Priority

The `priority` attribute of a Task is an integer ranging from 1 to 10, with 10 being the highest priority. This allows for fine-grained control over task execution order and importance. The default priority is 5 if not specified.
