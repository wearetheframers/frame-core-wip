---
title: Mind
publish: true
---

# Mind

## Overview

The Mind package represents the cognitive processes of a Framer. It manages thoughts, decision-making processes, and perceptions, playing a crucial role in how the Framer interacts with its environment and makes decisions.

## Key Features

- **Thought Management**: Stores and processes thoughts to guide decision-making.
- **Perception Processing**: Integrates sensory input to inform cognitive processes.
- **Decision Support**: Assists in making informed decisions based on thoughts and perceptions.

## Usage

To use the Mind class, integrate it with the Framer's components:

```python
from frame.src.framer.brain.mind.mind import Mind

mind = Mind()
mind.think("This is a new thought.")
current_thought = mind.get_current_thought()
print(current_thought)
```

## API Documentation

::: frame.src.framer.brain.mind.Mind
