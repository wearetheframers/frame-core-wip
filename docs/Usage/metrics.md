# LLM Metrics and API Cost Tracking

Frame CLI automatically tracks and reports LLM (Language Model) usage metrics and associated API costs. This feature helps users monitor their resource utilization and manage expenses when working with various language models.

## Why We Track Metrics

1. Cost Management: Tracking API costs helps users budget and optimize their usage of language models.
2. Performance Monitoring: Usage metrics provide insights into how frequently different models are called, which can be useful for performance tuning.
3. Transparency: Clear reporting of API calls and costs ensures users are aware of their resource consumption.

## How Metrics Are Tracked

The Frame CLI uses the `LLMMetrics` class to track usage metrics. This class maintains counters for API calls and costs for each model used. The metrics are updated in real-time as the Framer makes API calls to language models.

## Accessing Metrics

LLM usage metrics are automatically displayed after each `run-framer` or `run-framer-json` command execution. The metrics include:

- Total number of API calls
- Total cost across all models
- Breakdown of calls and costs for each individual model used

You can also access these metrics programmatically using the `get_metrics()` method of the `Frame` class.

## Example Metrics Output

```
LLM Usage Metrics:
Total calls: 5
Total cost: $0.0350
  gpt-3.5-turbo: 3 calls, $0.0150
  gpt-4: 2 calls, $0.0200
```

## Interpreting the Metrics

- "Total calls" represents the sum of all API calls made during the execution.
- "Total cost" is the cumulative cost of all API calls across all models.
- Each model used is listed with its specific number of calls and associated cost.

## Using Metrics for Optimization

By reviewing these metrics, users can:
1. Identify which models are used most frequently.
2. Understand the cost implications of their model choices.
3. Make informed decisions about model selection for different tasks.
4. Optimize prompts and workflows to reduce unnecessary API calls.

## Cost Calculation

Costs are calculated based on the number of tokens used and the specific pricing for each model. The `calculate_cost()` function in `llm_utils.py` handles this calculation, using a predefined cost structure for various models.

## Customizing Cost Tracking

Advanced users can modify the `cost_per_1k_tokens` dictionary in `llm_utils.py` to update pricing or add new models as needed.

Remember that costs may vary based on the specific models used and their current pricing. Always refer to the official pricing documentation of the respective API providers for the most up-to-date cost information.
