# Context Service

The Context Service manages roles and goals for Framers, facilitating communication between the Brain, Soul, and Agency through the `ContextService`.

## Usage

To use the Context Service, instantiate it and use its methods to manage roles and goals:

```python
context_service = Context()
context_service.set_roles(["role1", "role2"])
context_service.set_goals(["goal1", "goal2"])
```

## Related Components

- **Brain**: Communicates with the Context Service for decision-making processes.
- **Soul**: Interacts with the Context Service to provide a cohesive personality and emotional intelligence.
- **Agency**: Uses the Context Service to manage tasks and workflows.

## API Documentation

::: frame.src.services.context.context_service.Context

