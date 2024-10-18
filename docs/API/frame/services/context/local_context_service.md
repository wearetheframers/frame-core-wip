# Local Context Service

The Local Context Service module provides the `LocalContext` class, which manages local context for agent components, allowing them to share information with each other. It serves as a base class for more specialized local contexts.

## Usage

To use the Local Context Service, instantiate it and use its methods to manage context data:

```python
from frame.src.services.context.local_context_service import LocalContext

# Create a new local context
local_context = LocalContext()

# Set a value in the context
local_context.set("key", "value")

# Get a value from the context
value = local_context.get("key")

# Check if a key exists in the context
exists = local_context.has("key")

# Remove a key from the context
local_context.remove("key")

# Clear all data from the context
local_context.clear()
```

## Related Components

- **Brain**: May use LocalContext to store and retrieve temporary information during decision-making processes.
- **Agency**: Can utilize LocalContext to share data between different tasks or workflows.
- **Plugins**: May use LocalContext to store plugin-specific data that needs to be shared between different components.

## API Documentation

::: frame.src.services.context.local_context_service.LocalContext
    options:
      show_root_heading: true
      show_source: false
