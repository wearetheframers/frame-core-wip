---
title: Hugging Face Adapter
publish: true
---

# Hugging Face Adapter

## Overview

The HuggingFaceAdapter class provides methods to interact with Hugging Face models, including setting the default model and generating completions with retry logic. It implements rate limiting using a token bucket algorithm.

## Key Features

- **Rate Limiting**: Controls the rate of requests to the Hugging Face service.
- **Retry Logic**: Handles exceptions and retries operations with exponential backoff.
- **Model Interaction**: Supports interaction with various Hugging Face models.

## Usage

To use the HuggingFaceAdapter class, initialize it with the necessary API key and configuration:

```python
from frame.src.services.llm.llm_adapters.huggingface.huggingface_adapter import HuggingFaceAdapter, HuggingFaceConfig

config = HuggingFaceConfig(model="gpt2")
adapter = HuggingFaceAdapter(huggingface_api_key="your_huggingface_api_key")

completion = await adapter.get_completion(prompt="Hello, world!", config=config)
```

## API Documentation

::: frame.src.services.llm.llm_adapters.huggingface.huggingface_adapter.HuggingFaceAdapter
