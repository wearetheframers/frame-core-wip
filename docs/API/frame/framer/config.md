---
title: Config
publish: true
---

# Config

## Overview

The Config module provides configuration settings for the [[framer|Framer]], allowing for customization and flexibility in how [[framer|Framers]] are initialized and managed.

## Key Features

- **Customizable Settings**: Define settings for [[agency|roles]], [[agency|goals]], models, and more.
- **Flexible Initialization**: Use configuration settings to initialize [[framer|Framers]] with specific attributes and behaviors.

## Usage

To use the Config module, create a FramerConfig instance with the desired settings:

```python
from frame.src.framer.config import FramerConfig

config = FramerConfig(
    name="Example Framer",
    description="A sample Framer for demonstration purposes",
    default_model="gpt-3.5-turbo"
)
```

## Related Components

- [[framer]]: The main AI agent that uses the Config for initialization and behavior settings.
- [[agency]]: Uses the Config to set up roles and goals for the [[framer|Framer]].
- [[frame]]: The main interface that uses Config to create and manage [[framer|Framer]] instances.

## API Documentation

::: frame.src.framer.config.FramerConfig
