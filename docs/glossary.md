---
title: Glossary
weight: 90
---

# [[Glossary]]

## Core Components

### Frame

The main interface for creating and managing [[Framer]] instances. It acts as the central hub for initializing and orchestrating the various components of the framework.

### Framer

Represents an individual AI agent with capabilities for task management, decision-making, and interaction with language models. Each [[Framer]] operates independently but can collaborate with others.

### Framed

A collection of [[Framer]] objects working together to achieve complex tasks. It enables coordination and communication between multiple Framers, allowing for scalable and collaborative operations.

## Framer Components

### Agency

The decision-making and task management component of a [[Framer]]. It manages roles, goals, tasks, and workflows for the Framer.

### Soul

Manages memory and emotional states of a [[Framer]]. It interacts with the [[Brain]] and [[Agency]] to provide a cohesive personality and emotional intelligence.

### Brain

Handles decision-making processes for the [[Framer]], communicating with the [[Soul]] and [[Agency]] through the [[ContextService]].

### ActionRegistry

A component responsible for managing and executing actions within the Frame framework. It allows for the registration, retrieval, and execution of actions.

### FramerFactory

A factory class for creating [[Framer]] instances. It encapsulates the logic for constructing Framer objects, ensuring that all necessary components are properly initialized.

### FramerBuilder

A builder class for constructing [[Framer]] instances. It provides a flexible interface for configuring and creating Framer objects using the [[FramerFactory]].

### Perception

Represents sensory input or information received by a [[Framer]]. It is processed by the [[Mind]] to generate thoughts and decisions.

### Decision

Represents a decision made by the [[Brain]] component of a [[Framer]]. It includes an action, parameters, reasoning, confidence (default 0.7), priority (default 1), and expected results.

### Mind

Represents the cognitive processes of a Framer, including [[perception]] handling and thought processes.

### Memory

Manages memory storage and retrieval, supporting both global and multi-user contexts through the `MemoryService` and `Mem0Adapter`.

### Workflow

A sequence of related [[tasks]] that need to be completed to achieve a specific goal. It manages the execution and state of its tasks.

### WorkflowManager

Manages a sequence of related [[tasks]] within a [[Framer]], ensuring they are executed in the correct order and state.

### Task

An actionable item that Framers work on. It includes a description of the action to be performed, a priority level, a status, and can store results and metadata.

### Perception

Represents sensory input or information received by a Framer. It is processed by the [[Mind]] to generate thoughts and decisions.

### ContextService

Manages roles and goals for Framers, facilitating communication between the [[Brain]], [[Soul]], and [[Agency]] through the `ContextService`.

### SharedContextService

Extends [[ContextService]] to manage shared roles and goals across multiple Framers, enabling data sharing and collaboration through the `SharedContextService`.

## Services

### LLM Service

Manages interactions with various language models, providing methods to set the default model and generate text completions.

### LLM Adapter

Adapters for interacting with language models, including DSPy, HuggingFace, and LMQL. They provide methods for generating completions and managing rate limiting.

### LMQL Adapter

An adapter for LMQL operations with rate limiting. It provides methods to interact with LMQL models, including setting the default model, retrieving API keys, and generating completions with retry logic.

### HuggingFace Adapter

An adapter for Hugging Face operations with rate limiting. It provides methods to interact with Hugging Face models, including setting the default model and generating completions with retry logic.

### Token Bucket

Implements a token bucket algorithm for rate limiting. It is used to control the rate of requests to various services.

### Decision

Represents a decision made by the [[Brain]] component of a Framer. It includes an action, parameters, reasoning, confidence (default 0.7), priority (default 1), and expected results.

### MemoryAdapter

An interface for different [[memory]] storage backends, allowing the Framer to store and retrieve information efficiently.

### MemoryService

A service that manages [[memory]] operations, including storage, retrieval, and context management for Framers.

### Mem0Adapter

An adapter for basic [[memory]] operations, providing methods to interact with the memory storage, including adding, retrieving, and searching memories.

## Other Concepts

### Confidence

A measure of certainty associated with a decision or action taken by a Framer. It is expressed as a float value between 0 and 1.

### Priority

A numeric value representing the importance or urgency of a task, goal, or decision. Higher values indicate higher priority.
