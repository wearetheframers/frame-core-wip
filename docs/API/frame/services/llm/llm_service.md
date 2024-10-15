---
title: LLM Service
category: Services
weight: 3
publish: true
---

# LLM Service

## Overview

The LLM Service is a core component responsible for managing interactions with various language models. It abstracts the complexity of dealing with different APIs and provides a unified interface for generating text completions. This service is crucial for enabling the Framer to perform language-based tasks effectively.

## Key Components

- **openai_api_key**: API key for OpenAI services.
- **mistral_api_key**: API key for Mistral services.
- **huggingface_api_key**: API key for Hugging Face services.
- **default_model**: The default model to use for operations.

## LLM Adapters

The LLM Service uses adapters to interact with different language model providers. These adapters abstract the complexity of dealing with various APIs and provide a unified interface for generating text completions.

### Available Adapters

- **DSPyAdapter**: Adapter for DSPy operations with rate limiting. Note: DSPy does not support streaming mode. When streaming is enabled in other adapters, the `_streamed_response` variable in `Framer` accumulates the streamed content and resets with each new `get_completion` call. This variable is a dictionary with keys `status` and `result`.
- **ActionRegistry**: Manages and executes actions within the Frame framework.
- **HuggingFaceAdapter**: Adapter for Hugging Face operations with rate limiting.
- **LMQLAdapter**: Adapter for LMQL operations with rate limiting.

## How It Works

The LLM Service initializes with API keys for different language model providers. It allows setting a default model and provides methods to generate text completions. The service handles retries and error management to ensure robust interactions with the language models.

## Usage

To use the LLM Service, initialize it with the necessary API keys and call the `get_completion` method with the desired prompt and model settings. The service will handle the request and return the generated text.

### The `get_completion` Method

The `get_completion` method is a crucial part of the LLM Service. It handles the generation of text completions based on the given prompt and various parameters. Here's a detailed overview of its functionality:

```python
async def get_completion(
    self,
    prompt: str,
    model: str = None,
    max_tokens: int = 1024,
    temperature: float = 0.7,
    additional_context: Optional[Dict[str, Any]] = None,
    expected_output: Optional[str] = None,
    use_local: bool = False,
    stream: bool = False,
    include_frame_context: bool = False,
    recent_memories: Optional[List[Dict[str, Any]] = None,
) -> Union[str, Dict[str, Any], AsyncGenerator[str, None]]:
```

Key features:
- Supports various models (OpenAI, Mistral, Hugging Face)
- Handles streaming output when `stream=True`
- Incorporates additional context and recent memories into the prompt
- Supports local model usage with `use_local=True`
- Allows specifying expected output format

The method prepares a full prompt by combining the input prompt with optional Frame context and recent memories. It then selects the appropriate adapter (LMQL, DSPy, or Hugging Face) based on the model and parameters, and generates the completion.

When streaming is enabled, the method returns an async generator that yields chunks of the response as they become available. For non-streaming requests, it returns the full response as a string or dictionary.

## API Documentation

::: frame.src.services.llm.main.LLMService
