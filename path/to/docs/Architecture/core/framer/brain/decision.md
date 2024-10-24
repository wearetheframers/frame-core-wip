---
title: Decision
weight: 45
---

# Decision Architecture

## Overview

The Decision component represents a decision made by the Brain component of a Framer. It includes an action, parameters, reasoning, confidence, priority, and expected results.

## Key Features

- **Parameter Validation**: This feature ensures that all action parameters are not only present but also conform to the expected data types and formats. It checks for required fields, validates data types (e.g., strings, integers, lists), and can even enforce value ranges or specific formats (like regex for strings). This validation process helps prevent runtime errors and ensures that the actions can be executed reliably. If any parameters are missing or invalid, the system can provide informative error messages to guide users in correcting their input.
  
- **Context-Aware Decision Making**: The decision-making process is enhanced by the Framer's ability to understand its current context, which includes its roles, goals, and available actions. This means that the Framer can adapt its decisions based on the specific situation it finds itself in. For example, if the Framer is in a role that prioritizes user engagement, it may choose actions that foster interaction over those that are more analytical. This adaptability ensures that the Framer's responses are relevant and tailored to the user's needs.

- **Priority Management**: Actions can be prioritized to influence decision-making, ensuring that more critical actions are preferred.

- **Execution Modes**: The Framer supports multiple execution modes, allowing for flexibility in how decisions are carried out. Automatic execution means that decisions are implemented without user intervention, which is ideal for routine tasks. User approval mode requires confirmation from the user before proceeding, ensuring that critical actions are vetted. Deferred execution allows the Framer to postpone actions until certain conditions are met, which is useful in dynamic environments where immediate execution may not be appropriate.

- **Plugin Integration**: The Framer's architecture allows for seamless integration with various plugins, which can extend its functionality. This means that actions provided by plugins can be incorporated into the decision-making process, allowing for a richer set of capabilities. For instance, a plugin might offer specialized data analysis tools, and the Framer can decide to use these tools based on the context of the decision. This extensibility ensures that the Framer can evolve and adapt to new requirements without needing significant architectural changes.

- **Permission-Based Decision Making**: The Framer's permissions are considered when making decisions, ensuring it only chooses actions it's allowed to perform.

- **Task Creation**: Decisions can lead to the creation of tasks within the Agency's task management system.

## Parameter Validation

The Decision component now performs validation of action parameters. When a decision is made, the parameters associated with the chosen action are checked to ensure they meet the expected format and contain all required fields. If invalid parameters are detected, the decision can be adjusted or flagged for correction, preventing execution errors and enhancing system robustness.

## Decision Execution in Framer

In the Framer architecture, decisions are central to the operation of the AI agent. A decision is a structured plan of action that the agent intends to execute based on its current perception and context. However, there are scenarios where a decision might not be executed immediately, leading to another decision being made. These scenarios include:

1. **Decision Already Executed**: If a decision has already been executed, the system will skip re-execution to prevent redundant actions. This is typically logged with a message like "Decision already executed, skipping re-execution."

2. **Framer Not Ready**: If the Framer is not in a state to execute decisions (e.g., during initialization or when certain dependencies are not yet loaded), the decision will be queued for later execution.

3. **Invalid Decision**: If the decision is deemed invalid due to missing or incorrect parameters, it may be discarded, prompting the system to make a new decision.

4. **Priority Override**: In some cases, a new perception or context change might lead to a higher-priority decision overriding the current one, causing the system to pivot to the new decision.

## Related Components

- [[brain]]: Handles decision-making processes for the Framer, which can lead to task creation.
- [[action]]: Represents actionable items for Framers to work on, created as a result of decisions.
