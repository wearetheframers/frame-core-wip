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

The `priority` attribute of a Task uses the same priority system as roles and goals (LOW, MEDIUM, HIGH, CRITICAL). This allows for consistent prioritization across different components of the Framer. The priority of a task influences its execution order and importance within workflows. The default priority is MEDIUM if not specified.

Tasks with higher priorities are generally executed before those with lower priorities, allowing the Framer to focus on the most important or urgent tasks first. This priority system enables dynamic and context-aware task management, where the Framer can adjust its focus based on the current priorities of active tasks, roles, and goals.
