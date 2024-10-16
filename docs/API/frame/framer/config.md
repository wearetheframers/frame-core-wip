---
title: Config
publish: true
---

# Config

## Overview

The Config module provides configuration settings for the [[framer|Framer]], allowing for customization and flexibility in how [[framer|Framers]] are initialized and managed.

## Key Features

- **Customizable Settings**: Define settings for [[agency|roles]], [[agency|goals]], models, and more.
- **Flexible Initialization**: Use configuration settings to initialize [[framer|Framers]] with specific attributes and behaviors, excluding soul seed.

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

## Closing the Framer

The `close` method is used to optimize and clear all memory for the Framer. It ensures that all tasks and workflows are closed properly, and any resources or memory used by the Framer are released. This method should be called when the Framer is no longer needed to prevent memory leaks and ensure optimal performance. It is important to call this method to gracefully shut down the Framer.

```python
framer = Framer(config, llm_service, agency, brain, soul, workflow_manager)
# Perform tasks with the Framer
# ...
await framer.close()  # Optimize and clear memory
```

## Related Components

- [[framer]]: The main AI agent that uses the Config for initialization and behavior settings.
- [[agency]]: Uses the Config to set up roles and goals for the [[framer|Framer]].
- [[frame]]: The main interface that uses Config to create and manage [[framer|Framer]] instances.

## API Documentation

::: frame.src.framer.config.FramerConfig
