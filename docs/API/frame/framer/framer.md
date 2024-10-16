# Framer

## API Documentation

::: frame.src.framer.Framer
    options:
      show_root_heading: false
      show_source: false
# Framer Class

The `Framer` class represents an AI agent with cognitive capabilities. It integrates various components such as agency, brain, soul, and workflow management to create a comprehensive AI entity capable of processing perceptions, making decisions, and executing tasks.

## Key Features

- **Initialization, Acting, and Halting**: Framers are initialized using the `initialize()` method, which automatically calls `act()`, allowing them to make decisions from new perceptions. To stop the Framer from acting or making new tasks, use the `halt()` method. When halted, perceptions are still registered and can be considered in future decisions unless `ignore_perceptions_while_halted` is set to True.

- **Perception Handling**: The Framer can process perceptions through the `sense()` method. These perceptions are used to make decisions when the Framer is active. Observers can be notified of events such as `on_framer_opened` and `on_framer_closed`.

- **Configuration**: Framers are highly configurable through the `FramerConfig` class, allowing for customization of roles, goals, and other attributes.

- **Execution Control**: Framers have a `can_execute` property that determines if decisions are executed automatically. By default, this is set to `True`.

- **Integration with Services**: The Framer class integrates with various services such as LLMService, MemoryService, EQService, and ActionRegistry to enhance its capabilities. Note: DSPy does not support streaming mode. When streaming is enabled, the `_streamed_response` variable accumulates the streamed content and resets with each new `get_completion` call.

- **Automatic Role and Goal Generation**: If roles or goals are not provided during initialization, they will be automatically generated:
  - If both roles and goals are None, they will be generated using `generate_roles_and_goals()`.
  - If roles is an empty list `[]`, no roles or goals will be assigned, as the Framer has no roles to base goals on.
  - If goals is an empty list `[]` and roles is None, roles will be generated and goals will be generated based on these roles.
  - If both roles and goals are empty lists `[]`, both will be generated.
  - If roles are None or an empty list and goals are provided, roles will be generated and new goals will be added to the existing ones.
  - If either roles or goals is provided (not None or empty list), the provided value will be used.

- **Initialization**: The `initialize()` method is called after creating a Framer to ensure proper setup of roles and goals. This method handles various scenarios of role and goal initialization based on the provided or existing values. The `act()` method is automatically called during initialization to ensure the Framer starts acting immediately.

## Attributes

- `ignore_perceptions_while_halted`: A boolean attribute that determines whether perceptions should be ignored while the Framer is halted. Default is False.
- `can_execute`: A boolean attribute that determines whether decisions are executed automatically. Default is True.

## Methods

- `act()`: Activates the Framer, allowing it to make decisions from new perceptions. This method sets the Framer to an active state, enabling it to respond to perceptions and execute tasks. It is automatically called during initialization to ensure the Framer starts acting immediately.
- `halt()`: Halts the Framer, pausing decision-making from new perceptions.
- `sense(perception)`: Processes a perception and makes a decision if the Framer is active. The Framer must be acting to respond to perceptions.
