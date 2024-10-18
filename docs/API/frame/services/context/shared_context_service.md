# Shared Context Service

The Shared Context Service extends the Context Service to manage shared roles and goals across multiple Framers, enabling data sharing and collaboration through the `SharedContextService`.

## Usage

To use the Shared Context Service, instantiate it and use its methods to manage shared roles and goals, taking into account Framer IDs to associate contexts with specific Framers:

```python
shared_context_service = SharedContext()
shared_context_service.set_shared_roles("framer_id_1", ["role1", "role2"])
shared_context_service.set_shared_goals("framer_id_1", ["goal1", "goal2"])
```

## Related Components

The `shared_context` service functions like a plugin but does not require explicit permissions to be accessed. It is always available to Framers, enabling them to manage shared roles and goals effectively.

- **Context Service**: Provides the base functionality for managing roles and goals.
- **Framer**: Uses the Shared Context Service to collaborate with other Framers.

## API Documentation

::: frame.src.services.context.shared_context_service.SharedContext
