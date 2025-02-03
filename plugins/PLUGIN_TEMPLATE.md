# Frame Plugin Template

## Overview

Brief description of what your plugin does and its main features.

## Installation

```bash
pip install frame-ai-plugin-[name]
```

## Requirements

List any additional requirements or dependencies:

```txt
dependency1>=1.0.0
dependency2>=2.0.0
```

## Usage

Basic example of how to use the plugin:

```python
from frame import Frame
from frame.framer.config import FramerConfig

frame = Frame()
config = FramerConfig(
    name="MyFramer",
    permissions=["with_your_plugin"]
)
```

## Configuration

Document any configuration options:

```python
frame = Frame(
    plugin_config={
        "your_plugin": {
            "option1": "value1",
            "option2": "value2"
        }
    }
)
```

## Actions

List and describe the actions your plugin provides:

- `action_name`: Description of what this action does
- `another_action`: Description of another action

## Permissions

List required permissions:

- `with_your_plugin`: Base permission to use this plugin
- `with_your_plugin_feature`: Permission for specific feature

## Development

Instructions for developing/extending the plugin.

## Testing

How to run the plugin's tests:

```bash
pytest tests/test_your_plugin.py
```

## License

Specify the license (should match Frame's licensing).
