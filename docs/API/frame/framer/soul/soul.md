# Soul Module

The Soul module is a core component of the Frame-Core system, responsible for managing the intrinsic characteristics and identity of a Framer.

## Overview

The Soul module provides functionalities to define and manage the unique identity and intrinsic characteristics of a Framer. It interacts with other components to ensure that the Framer's actions and decisions align with its core identity.

## Usage

To utilize the Soul module within the Frame-Core system, you can follow this example:

```python
from frame.src.framer.soul.soul import Soul

# Initialize a new Soul with default seed
soul = Soul()

# Initialize a new Soul with custom seed
soul_custom = Soul(seed="You are an expert in artificial intelligence")

# Access Soul attributes
print(f"Seed: {soul.seed}")
print(f"Custom Seed: {soul_custom.seed}")

# Update Soul state
soul.state["mood"] = "enthusiastic"
```

## Default Behavior

If no seed is provided, the Soul will initialize with a default seed, which is typically set in the Framer's configuration.

## API Documentation

::: frame.src.framer.soul.Soul
