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

## API Documentation

::: frame.src.services.llm.main.LLMService
