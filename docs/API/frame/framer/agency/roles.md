# Roles

::: frame.src.framer.agency.roles.Role
    options:
      show_root_heading: false
      show_source: false

## Overview

The `Role` module is responsible for defining and managing the roles that a Framer can assume. Roles help guide the Framer's behavior and decision-making processes by providing context and constraints.

### Attributes

- `id` (str): The unique identifier for the role.
- `name` (str): The name of the role.
- `description` (str): A detailed description of the role.
- `permissions` (List[str]): A list of permissions associated with the role.
- `priority` (Priority): The priority level of the role.
- `status` (RoleStatus): The current status of the role (ACTIVE, INACTIVE, or SUSPENDED).

## RoleStatus

::: frame.src.framer.agency.roles.RoleStatus
    options:
      show_root_heading: false
      show_source: false

An enumeration representing the possible statuses of a role:

- `ACTIVE`: The role is currently active and being used.
- `INACTIVE`: The role is not currently active but can be reactivated.
- `SUSPENDED`: The role has been temporarily suspended and cannot be used.
