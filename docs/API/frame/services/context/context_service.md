# Local Context Service

::: frame.src.services.context.local_context_service.LocalContext
    options:
      show_root_heading: false
      show_source: false

## Overview

The Local Context Service module provides the LocalContext class, which manages local context for agent components, allowing them to share information with each other. It serves as a base class for more specialized local contexts.

## Key Features

- Manages local context for agent components
- Provides methods for adding, removing, and retrieving context information
- Allows for the evaluation of context relevance

## Usage

To use the Local Context Service:

```python
from frame.src.services.context.local_context_service import LocalContext

local_context = LocalContext()
local_context.add_context({"key": "user_preference", "value": "dark_mode"})
local_context.add_context({"key": "last_interaction", "value": "2023-04-01 14:30:00"})

context_info = local_context.get_context()
```

## Methods

- `add_context(context: Dict[str, Any])`: Add new context information
- `remove_context(key: str)`: Remove context information by key
- `get_context() -> List[Dict[str, Any]]`: Get all context information
- `evaluate_context() -> List[Dict[str, Any]]`: Evaluate the relevance of context information
