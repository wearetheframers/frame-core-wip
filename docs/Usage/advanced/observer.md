# Observer Events

Observer events in the Frame framework allow external components to be notified of significant changes or actions within a Framer. This mechanism enables better integration and interaction with other systems or components.

## Available Observer Events

### on_framer_opened
- **Description**: Triggered when a Framer is initialized and ready to act.
- **Use Case**: Useful for setting up any necessary state or resources when a Framer starts.

### on_framer_closed
- **Description**: Triggered when a Framer is closed and resources are released.
- **Use Case**: Ideal for cleaning up resources or saving state when a Framer is no longer needed.

### on_decision_made
- **Description**: Triggered when a decision is made by the Framer.
- **Use Case**: Allows external systems to react to decisions, such as logging or triggering additional actions.

### on_task_completed
- **Description**: Triggered when a task is completed by the Framer.
- **Use Case**: Can be used to update task management systems or notify users of task completion.

### on_error_occurred
- **Description**: Triggered when an error occurs during Framer operations.
- **Use Case**: Useful for error logging and handling, allowing systems to respond to issues promptly.

## Implementing Observers

To implement an observer, define a function that matches the signature of the event you want to observe. Then, add the observer to the Framer using the `add_observer` method.

```python
def my_observer(decision):
    print(f"Decision made: {decision}")

framer.add_observer(my_observer)
```

Observers can be removed using the `remove_observer` method.

```python
framer.remove_observer(my_observer)
```
