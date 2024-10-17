# ExecutionContextService

::: frame.src.services.context.execution_context_service.ExecutionContextService
    options:
      show_root_heading: false
      show_source: false

## Overview

The ExecutionContextService is a crucial component in the Frame framework that provides a shared context for executing actions across different components of a Framer. It encapsulates various services and state information necessary for action execution.

## Key Features

- Manages shared state across Framer components
- Provides access to essential services (LLM, memory, EQ)
- Facilitates consistent execution of actions

## Usage

To use the ExecutionContextService:

```python
from frame.src.services.context.execution_context_service import ExecutionContextService
from frame.src.services.llm.main import LLMService
from frame.src.framer.soul.soul import Soul

llm_service = LLMService()
soul = Soul()

execution_context = ExecutionContextService(llm_service=llm_service, soul=soul)

# Now you can use the execution_context in your actions or other components
result = await some_action(execution_context, other_params)
```

## Methods

- `__init__(self, llm_service: LLMService, soul: Optional[Soul] = None, state: Optional[Dict[str, Any]] = None)`: Initialize the ExecutionContextService with necessary services and state.
- `get_state() -> Dict[str, Any]`: Retrieve the current state.
- `update_state(new_state: Dict[str, Any]) -> None`: Update the current state with new information.
- `get_llm_service() -> LLMService`: Get the LLM service instance.
- `get_soul() -> Optional[Soul]`: Get the Soul instance if available.

## Related Components

- Agency: Uses ExecutionContextService for action execution.
- ActionRegistry: Utilizes ExecutionContextService to provide context for registered actions.
- Framer: Initializes and manages the ExecutionContextService for its components.
