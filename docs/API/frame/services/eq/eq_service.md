# EQ Service

## Overview

The EQ (Emotional Intelligence) Service is designed to enhance the emotional intelligence capabilities of the Framer framework. It provides tools for sentiment analysis and emotional state tracking, allowing Framers to better understand and respond to emotional cues in text.

## Key Features

- Sentiment analysis using various adapters
- Emotional state tracking and management
- Integration with the Framer framework for enhanced decision-making

## Adapters

### Naive Adapter

The Naive Adapter is a basic sentiment analysis tool that detects simple emotional cues in text. It updates the emotional state based on keywords and provides a foundation for more advanced analysis.

## Usage Example

```python
from frame.src.services.eq.eq_adapters import SentimentAnalysisAdapter

# Initialize the adapter
adapter = SentimentAnalysisAdapter()

# Analyze text
emotions = adapter.analyze("I am very happy today!")
print(emotions)
```

This example demonstrates how to use the Naive Adapter to analyze text and update the emotional state.

## API Documentation

::: frame.src.services.eq
