---
title: Perception
publish: true
---

# Perception

## Overview

The Perception class represents the perceptual input processed by the Framer's Mind. It is responsible for capturing and interpreting sensory data, which is then used to inform the Framer's cognitive processes and decision-making.

## Key Features

- **Sensory Input**: Captures data from various sources to provide context for the Framer.
- **Data Interpretation**: Analyzes and interprets sensory data to inform decisions.
- **Integration with Mind**: Works closely with the Mind to process perceptions and generate thoughts.

## Usage

To use the Perception class, create an instance and process sensory data:

```python
from frame.src.framer.brain.perception import Perception

perception = Perception(type="visual", data={"image": "path/to/image.jpg"})
mind.process_perception(perception)
```

## API Documentation

::: frame.src.framer.brain.perception.Perception
