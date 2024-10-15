# SyncFrame Documentation

The `SyncFrame` package provides a synchronous interface for the [[frame|Frame]] framework, allowing for easier integration with synchronous code or simpler use cases. It wraps the asynchronous core of [[frame|Frame]] to provide a synchronous API.

## Usage

```python
from frame.sync_frame import SyncFrame

def sync_example():
    sync_frame = SyncFrame()
    framer = sync_frame.create_framer(
        config={"name": "SyncFramer", "default_model": "gpt-3.5-turbo"},
        soul_seed={"seed": "You are a helpful AI assistant."}
    )
    
    result = sync_frame.perform_task(framer, {"description": "Summarize synchronous programming benefits"})
    print(f"Task result: {result}")

    perception = {"type": "input", "description": "Compare programming paradigms"}
    tasks = sync_frame.generate_tasks_from_perception(framer, perception)
    for task in tasks:
        result = sync_frame.perform_task(framer, task)
        print(f"Task '{task['description']}' result: {result}")

# Run the sync example
sync_example()
```

The synchronous interface (`sync_frame`) is built on top of the asynchronous core. It uses Python's `asyncio.run()` to execute asynchronous [[framer|functions]] in a synchronous context.

## API Documentation

::: frame.sync_frame.SyncFrame
