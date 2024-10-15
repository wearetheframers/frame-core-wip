---
title: LMQL Adapter
publish: true
---

# LMQL Adapter

## Overview

The LMQLAdapter class provides methods to interact with LQML models, including setting the default model, retrieving API keys, and generating completions with retry logic. It implements rate limiting using a token bucket algorithm.

## Key Features

- **Rate Limiting**: Controls the rate of requests to the LQML service.
- **Retry Logic**: Handles exceptions and retries operations with exponential backoff.
- **Model Interaction**: Supports interaction with both OpenAI and Mistral models.

## Usage

To use the LMQLAdapter class, initialize it with the necessary API keys and configuration:

```python
from frame.src.services.llm.llm_adapters.lmql.lmql_adapter import LMQLAdapter, LMQLConfig

config = LMQLConfig(model="gpt-3.5-turbo")
adapter = LMQLAdapter(openai_api_key="your_openai_api_key", mistral_api_key="your_mistral_api_key")

completion = await adapter.get_completion(prompt="Hello, world!", config=config)
```

## API Documentation

::: frame.src.services.llm.llm_adapters.lmql.lmql_adapter.LMQLAdapter
