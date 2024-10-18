---
title: Perception
publish: true
---

# Perception

## Overview

The Perception class represents the perceptual input processed by the Framer's Mind. It is responsible for capturing and interpreting a wide range of data, which is then used to inform the Framer's cognitive processes and decision-making. 

In Frame, perceptions are not limited to human senses. They can be any type of information or stimulus that can be analyzed by the language model. This includes traditional inputs like text, images, or sounds, but also extends to more abstract or non-human sensory data such as magnetic fields, vibrations, internal states like hunger, or any other form of data.

The "prompt" action in a Framer is essentially processing a perception of hearing for text input and responding to it. However, the Perception class is designed to handle and represent this wide variety of potential inputs.

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
