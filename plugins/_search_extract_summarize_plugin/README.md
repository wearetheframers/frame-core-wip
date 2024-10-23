# SearchExtractSummarizePlugin

The SearchExtractSummarizePlugin is a powerful tool designed to enhance the capabilities of the Frame AI system by providing web search, information extraction, and summarization functionalities.

## Features

- Web search using a specified API
- Content scraping from web pages
- Text chunking for efficient processing
- Vector database storage for quick retrieval
- Language model-based summarization

## Installation

To use this plugin, ensure you have installed the required dependencies:

```bash
pip install requests beautifulsoup4 jinja2 openai vectordb python-dotenv
```

### Windows Users

If you're on Windows, you need to install Visual C++ Build Tools to use this plugin. You can download and install them from:

https://visualstudio.microsoft.com/visual-cpp-build-tools/

Make sure to select the "C++ build tools" workload during installation.

## Usage

1. Initialize the Frame and create a Framer instance:

```python
from frame import Frame
from frame.src.framer.config import FramerConfig
from frame.src.plugins.search_extract_summarize_plugin import SearchExtractSummarizePlugin

# Initialize Frame
frame = Frame()

# Create a Framer instance
config = FramerConfig(name="Research Assistant", default_model="gpt-3.5-turbo")
framer = await frame.create_framer(config)
```

2. Initialize the plugin with the Framer instance and register it:

```python
plugin = SearchExtractSummarizePlugin(framer)
framer.register_plugin("search_extract_summarize", plugin)
```

3. Use the plugin through the Framer:

```python
query = "Latest advancements in AI"
result = await framer.use_plugin("search_extract_summarize", query)
print(result)
```

## Configuration

The plugin uses a configuration system that prioritizes environment variables over a `config.json` file. The following configuration options are available:

- `SEARCH_API_KEY`: API key for the web search service
- `SEARCH_PROJECT_KEY`: Project key for the web search service
- `LLM_API_KEY`: API key for the language model service (e.g., OpenAI)
- `LLM_BASE_URL`: Base URL for the language model API (optional, defaults to OpenAI's URL)

To configure the plugin:

1. Set environment variables:
   You can set these in your system environment or in a `.env` file in the project root.

   Example `.env` file:
   ```
   SEARCH_API_KEY=your_search_api_key
   SEARCH_PROJECT_KEY=your_search_project_key
   LLM_API_KEY=your_llm_api_key
   LLM_BASE_URL=https://api.openai.com
   ```

2. Use `config.json`:
   If environment variables are not set, the plugin will look for a `config.json` file in its directory.

   Example `config.json`:
   ```json
   {
     "SEARCH_API_KEY": "your_search_api_key",
     "SEARCH_PROJECT_KEY": "your_search_project_key",
     "LLM_API_KEY": "your_llm_api_key",
     "LLM_BASE_URL": "https://api.openai.com"
   }
   ```

The plugin will first check for environment variables, and if not found, it will use the values from `config.json`. This allows for flexible configuration management across different environments.

## Contributing

Contributions to improve the SearchExtractSummarizePlugin are welcome. Please ensure that you add or update tests as necessary when making changes.

## License

This plugin is part of the Frame project and is subject to the same license as the main project.
