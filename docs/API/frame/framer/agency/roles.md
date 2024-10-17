# Roles

::: frame.src.framer.agency.roles.Roles
    options:
      show_root_heading: false
      show_source: false

## Overview

The `Roles` module is responsible for defining and managing the roles that a Framer can assume. Roles help guide the Framer's behavior and decision-making processes by providing context and constraints.

### Attributes

- `role_list` (List[Dict[str, Any]]): A list of roles with their descriptions and associated permissions.

## Methods

### `add_role`

Adds a new role to the list of roles.

### `remove_role`

Removes a role from the list by its identifier.

### `evaluate_roles`

Evaluates the current roles to determine their relevance and applicability.

## Usage

To add a new role:

```python
roles.add_role(
    {"name": "Data Analyst", "description": "Analyze data and generate insights", "permissions": ["read", "write"]}
)
```

To evaluate roles:

```python
applicable_roles = roles.evaluate_roles()
```
