# Plugin System Overview

Frame's plugin system is designed to be flexible and extensible, allowing developers to easily add new functionality to their Framer instances. By default, Frame looks for plugins in the `frame/src/plugins` directory within the library. However, this can be configured to look for plugins in any directory on the system.

## Plugin Configuration

Plugins can be configured using either environment variables or a `config.json` file within each plugin's directory. The system follows this priority order when looking for configuration:

1. Environment variables (highest priority)
2. `.env` file in the project root
3. `config.json` file in the plugin's directory

For example, to set the Google API key for a plugin, you can:

1. Set an environment variable: `GOOGLE_API_KEY=your_api_key_here`
2. Add it to your `.env` file: `GOOGLE_API_KEY=your_api_key_here`
3. Create a `config.json` file in the plugin's directory:

```json
{
  "GOOGLE_API_KEY": "your_api_key_here"
}
```

## Using Plugins

To use a plugin with a Framer instance, you need to:

1. Import the plugin
2. Initialize the plugin with the Framer instance
3. Register the plugin with the Framer

Here's an example using the `SearchExtractSummarizePlugin`:

```python
from frame import Frame
from frame.src.framer.config import FramerConfig
from frame.src.plugins.search_extract_summarize_plugin import SearchExtractSummarizePlugin

# Initialize Frame
frame = Frame()

# Create a Framer instance
config = FramerConfig(name="Research Assistant", default_model="gpt-3.5-turbo")
framer = await frame.create_framer(config)

# Initialize and register the plugin
search_plugin = SearchExtractSummarizePlugin(framer)
framer.register_plugin("search_extract_summarize", search_plugin)

# Use the plugin
result = await framer.use_plugin("search_extract_summarize", "Latest advancements in AI")
print(result)
```

For more details on specific plugins and how to create custom plugins, please refer to the other sections in this documentation.
