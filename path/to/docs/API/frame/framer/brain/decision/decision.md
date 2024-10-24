---
title: Decision
category: Core Components
weight: 3
publish: true
---

# Decision

The `Decision` component in Frame represents the outcome of processing perceptions and the current state of the Framer. It is responsible for determining the actions to be taken based on the information available to the Framer.

## Key Features

- **Parameter Validation**: This feature ensures that all action parameters are not only present but also conform to the expected data types and formats. It checks for required fields, validates data types (e.g., strings, integers, lists), and can even enforce value ranges or specific formats (like regex for strings). This validation process helps prevent runtime errors and ensures that the actions can be executed reliably. If any parameters are missing or invalid, the system can provide informative error messages to guide users in correcting their input.

- **Contextual Awareness**: The decision-making process is enhanced by the Framer's ability to understand its current context, which includes its roles, goals, and available actions. This means that the Framer can adapt its decisions based on the specific situation it finds itself in. For example, if the Framer is in a role that prioritizes user engagement, it may choose actions that foster interaction over those that are more analytical. This adaptability ensures that the Framer's responses are relevant and tailored to the user's needs.

- **Execution Modes**: The Framer supports multiple execution modes, allowing for flexibility in how decisions are carried out. Automatic execution means that decisions are implemented without user intervention, which is ideal for routine tasks. User approval mode requires confirmation from the user before proceeding, ensuring that critical actions are vetted. Deferred execution allows the Framer to postpone actions until certain conditions are met, which is useful in dynamic environments where immediate execution may not be appropriate.

- **Integration with Plugins**: The Framer's architecture allows for seamless integration with various plugins, which can extend its functionality. This means that actions provided by plugins can be incorporated into the decision-making process, allowing for a richer set of capabilities. For instance, a plugin might offer specialized data analysis tools, and the Framer can decide to use these tools based on the context of the decision. This extensibility ensures that the Framer can evolve and adapt to new requirements without needing significant architectural changes.

The `Decision` component now includes validation of action parameters. When a decision is made, it checks that all required parameters for the action are present and correctly formatted. This ensures that actions can be executed reliably and helps prevent runtime errors due to missing or invalid parameters.

The `Decision` component is designed to handle a wide variety of potential perceptions, which can include traditional inputs like text, images, or sounds, as well as more abstract or non-human sensory data such as magnetic fields, vibrations, or internal states.

::: frame.src.framer.brain.decision.Decision
