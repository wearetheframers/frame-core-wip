# Prompt Examples and Formatting Guide

This guide explains how to format prompts for different LLM adapters in the Frame framework. Proper formatting ensures that your prompts are processed correctly by the underlying models, including how to get JSON objects and structured data.

## Why Prompt Formatting Matters

Different LLM adapters and models have specific requirements or preferences for input formatting. By following these guidelines, you can:

1. Ensure compatibility with the chosen adapter/model
2. Improve the quality and consistency of generated responses
3. Take advantage of model-specific features or capabilities
4. Obtain structured data and JSON objects when needed

## LMQL Adapter

LMQL (Language Model Query Language) allows for more structured prompts and can include expected output formats, including JSON.

### Format for Text:
```python
prompt = '''"""Your prompt text here"""
[RESPONSE]
Expected output format (optional)
'''
```

### Example for Text:
```python
prompt = '''"""Generate a short story about a robot learning to paint."""
[RESPONSE]
A 3-paragraph story with a beginning, middle, and end.
'''
```

### Format for JSON:
```python
prompt = '''"""Your prompt text here"""
[RESPONSE]
json
{
    "key1": "value1",
    "key2": "value2"
}
'''
```

### Example for JSON:
```python
prompt = '''"""Provide information about a famous scientist."""
[RESPONSE]
json
{
    "name": str,
    "field": str,
    "notable_discovery": str,
    "birth_year": int
}
'''
```

## DSPy Adapter

DSPy uses standard string formatting for prompts, but you can specify JSON output in the prompt text.

### Format for Text:
```python
prompt = "Your prompt text here"
```

### Example for Text:
```python
prompt = "Explain the concept of quantum entanglement in simple terms."
```

### Format for JSON:
```python
prompt = "Your prompt text here. Provide the answer in JSON format with the following structure: {\"key1\": \"value1\", \"key2\": \"value2\"}"
```

### Example for JSON:
```python
prompt = "List three major programming languages. Provide the answer in JSON format with the following structure: {\"languages\": [\"language1\", \"language2\", \"language3\"]}"
```

## Hugging Face Adapter

Hugging Face models use standard string formatting for prompts, but you can request JSON output in the prompt text.

### Format for Text:
```python
prompt = "Your prompt text here"
```

### Example for Text:
```python
prompt = "Translate the following English text to French: 'Hello, how are you?'"
```

### Format for JSON:
```python
prompt = "Your prompt text here. Return the response as a JSON object with the following keys: key1, key2, key3"
```

### Example for JSON:
```python
prompt = "Provide information about the solar system. Return the response as a JSON object with the following keys: number_of_planets, largest_planet, smallest_planet"
```

## Best Practices

1. Be clear and specific in your prompts.
2. For LMQL, use the [RESPONSE] tag to guide the model's output format when needed.
3. When requesting JSON or structured data, clearly specify the expected format in your prompt.
4. Consider the model's context window size when crafting long prompts.
5. Test your prompts with different phrasings to find the most effective formulation.
6. Use appropriate formatting for each adapter to ensure optimal results.
7. When using LMQL, take advantage of its structured format to specify desired output more precisely.
8. For DSPy and Hugging Face, include explicit instructions for JSON formatting in the prompt text.
9. Always validate and parse the JSON responses in your code to handle potential formatting issues.

By following these formatting guidelines and best practices, you can ensure that your prompts are processed correctly and efficiently by the Frame framework, regardless of the underlying LLM adapter in use. This will lead to more accurate, relevant, and structured responses from the AI models, including JSON objects when needed.
