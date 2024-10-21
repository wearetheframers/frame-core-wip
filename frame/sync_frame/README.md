# SyncFrame Usage

The `SyncFrame` class provides a synchronous interface to the asynchronous operations of the `Frame` class, making it easier to use in synchronous contexts. This is particularly useful when you want to integrate Frame into applications that do not support asynchronous programming.

## Key Features

- **Synchronous Interface**: Provides a synchronous wrapper around the asynchronous `Frame` class.
- **Task Management**: Allows for synchronous task execution and perception processing.
- **Easy Integration**: Simplifies the integration of Frame into existing synchronous applications.

## Basic Usage

Here's a basic example of how to use `SyncFrame`:

```python
from frame.sync_frame import SyncFrame
from frame.src.framer.config import FramerConfig
from frame.src.services.llm.main import LLMService

# Initialize SyncFrame with an LLMService
llm_service = LLMService(api_key="your_api_key")
sync_frame = SyncFrame(llm_service=llm_service)

# Create a Framer instance
config = FramerConfig(name="Example Framer", default_model="gpt-4o-mini")
framer = sync_frame.create_framer(config)

# Define a task
task = {"description": "Engage in a deep conversation"}
result = sync_frame.perform_task(framer, task)
print(f"Task result: {result}")

# Process a perception
perception = {"type": "hearing", "data": {"text": "Hello, how are you?"}}
decision = sync_frame.process_perception(framer, perception)
print(f"Decision: {decision}")

# Clean up
sync_frame.close_framer(framer)
```

## Installation

Ensure you have the necessary dependencies installed. You can install them using:

```bash
pip install -r requirements.txt
```

## Advanced Features

- **Task Generation**: Generate tasks from perceptions synchronously.
- **Framer Management**: Create, manage, and close Framer instances easily.

For more detailed examples, refer to the examples directory.
