---
title: Decision
category: Core Components
weight: 3
publish: true
---

# Decision

The `Decision` component in Frame represents the outcome of processing perceptions and the current state of the Framer. It is responsible for determining the actions to be taken based on the information available to the Framer.

## Key Features

- **Parameter Validation**: Validates action parameters to ensure all necessary variables are present and correctly formatted before execution.
- **Contextual Awareness**: Takes into account the Framer's current roles, goals, and available actions when making decisions.
- **Execution Modes**: Supports various execution modes, including automatic execution, user approval, or deferred execution.
- **Integration with Plugins**: Allows for actions provided by plugins to be included in the decision-making process.

The `Decision` component now includes validation of action parameters. When a decision is made, it checks that all required parameters for the action are present and correctly formatted. This ensures that actions can be executed reliably and helps prevent runtime errors due to missing or invalid parameters.

The `Decision` component is designed to handle a wide variety of potential perceptions, which can include traditional inputs like text, images, or sounds, as well as more abstract or non-human sensory data such as magnetic fields, vibrations, or internal states.

::: frame.src.framer.brain.decision.Decision
