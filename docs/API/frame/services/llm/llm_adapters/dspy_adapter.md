---
title: DSPy Adapter
publish: true
---

# DSPy Adapter

## Overview

The DSPyAdapter class provides methods to interact with DSPy models, including generating completions with retry logic for handling exceptions. It implements rate limiting using a token bucket algorithm.

## Key Features

- **Rate Limiting**: Controls the rate of requests to the DSPy service.
- **Retry Logic**: Handles exceptions and retries operations with exponential backoff.
- **Model Interaction**: Supports interaction with DSPy models. Note: DSPy does not support streaming mode.

## Usage

To use the DSPyAdapter class, initialize it with the necessary API key and configuration:

```python
from frame.src.services.llm.llm_adapters.dspy.dspy_adapter import DSPyAdapter, DSPyConfig

config = DSPyConfig(model="gpt-3.5-turbo")
adapter = DSPyAdapter(openai_api_key="your_openai_api_key")

completion = await adapter.get_completion(prompt="Hello, world!", config=config)
```

## API Documentation

::: frame.src.services.llm.llm_adapters.dspy.dspy_adapter.DSPyAdapter
