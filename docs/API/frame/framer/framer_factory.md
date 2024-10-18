# FramerFactory

The `FramerFactory` is a crucial component in the Frame framework, responsible for creating and configuring Framer instances. It encapsulates the complex logic of Framer initialization, ensuring that all necessary components are properly set up and integrated.

## Overview

The FramerFactory provides a flexible and extensible way to create Framer instances with various configurations, including custom plugins. This design allows for the creation of highly customized Framers tailored to specific use cases or requirements.

## Key Features

- Encapsulated Framer creation logic
- Support for custom plugin integration
- Flexible configuration options
- Standardized Framer initialization process

## Usage

```python
from frame.src.framer.framer_factory import FramerFactory
from frame.src.framer.config import FramerConfig

# Create a FramerFactory instance
config = FramerConfig(name="CustomFramer", default_model="gpt-3.5-turbo")
factory = FramerFactory(config, llm_service)

# Create a Framer instance
framer = await factory.create_framer()

# Create a Framer with custom plugins
custom_plugin = CustomPlugin()
framer_with_plugin = await factory.create_framer(plugins=[custom_plugin])
```

## Plugin System

The FramerFactory supports a robust plugin system, allowing for extensive customization and expansion of Framer capabilities. This system is designed to be as flexible and powerful as mods in games, enabling developers to create a wide range of extensions and enhancements.

Plugins can be easily integrated during the Framer creation process, allowing for seamless extension of functionality.

## API Reference

::: frame.src.framer.framer_factory.FramerFactory
    options:
      show_root_heading: false
      show_source: false

For more detailed information on creating and using plugins, refer to the [[plugins]] documentation.
