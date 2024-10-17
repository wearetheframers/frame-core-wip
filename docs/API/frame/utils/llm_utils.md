# LLM Utils

## Overview

The `LLM Utils` module provides utility functions and classes for interacting with language models. It includes functions for calculating token sizes, tracking usage, and selecting the best model based on token count.

### Functions

#### `calculate_token_size`

::: frame.src.utils.llm_utils.calculate_token_size
    options:
      show_root_heading: false
      show_source: false

#### `choose_best_model_for_tokens`

::: frame.src.utils.llm_utils.choose_best_model_for_tokens
    options:
      show_root_heading: false
      show_source: false

#### `track_llm_usage`

::: frame.src.utils.llm_utils.track_llm_usage
    options:
      show_root_heading: false
      show_source: false

## Usage

To calculate the number of tokens in a text:

```python
token_count = calculate_token_size("This is a sample text.")
```

To choose the best model for a given token count:

```python
best_model = choose_best_model_for_tokens(token_count)
```

To track the usage of a language model:

```python
track_llm_usage("gpt-3.5-turbo", tokens_used=1500)
```
