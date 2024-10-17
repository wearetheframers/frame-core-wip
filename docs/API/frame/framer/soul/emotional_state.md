# Emotional State

## Overview

The `Emotional State` module is responsible for simulating and managing the emotional states of a Framer. This module allows Framers to exhibit more human-like interactions by incorporating emotions into their decision-making processes.

### Attributes

- `emotions` (Dict[str, float]): A dictionary of emotions with their intensity levels.

## Methods

### `set_emotional_state`

Sets the intensity level of a specific emotion.

### `get_emotional_state`

Retrieves the current intensity level of a specific emotion.

## Usage

To set an emotional state:

```python
emotional_state.set_emotional_state("happiness", 0.75)
```

To get an emotional state:

```python
current_happiness = emotional_state.get_emotional_state("happiness")
```
