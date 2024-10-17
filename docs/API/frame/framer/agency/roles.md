# Roles

::: frame.src.framer.agency.roles.Roles
    options:
      show_root_heading: false
      show_source: false

## Overview

The `Roles` module is responsible for defining and managing the roles that a Framer can assume. Roles help guide the Framer's behavior and decision-making processes by providing context and constraints.

### Attributes

- `roles` (List[Role]): A list of Role objects representing the current roles.

## Role

::: frame.src.models.framer.agency.roles.Role
    options:
      show_root_heading: false
      show_source: false

### Attributes

- `id` (str): The unique identifier for the role.
- `name` (str): The name of the role.
- `description` (str): A detailed description of the role.
- `permissions` (List[str]): A list of permissions associated with the role.
- `priority` (Priority): The priority level of the role.
- `status` (RoleStatus): The current status of the role (ACTIVE, INACTIVE, or SUSPENDED).

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
