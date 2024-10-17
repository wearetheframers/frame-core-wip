# Metrics

::: frame.src.utils.metrics
    options:
      show_root_heading: false
      show_source: false

## Overview

The `Metrics` module provides functionality for tracking and managing metrics related to the usage of language models and other components within the Frame framework. It includes classes and methods for updating, retrieving, and resetting metrics.

### Classes

#### `MetricsManager`

::: frame.src.utils.metrics.MetricsManager
    options:
      show_root_heading: false
      show_source: false

## Usage

To update metrics for a specific model:

```python
metrics_manager = MetricsManager()
metrics_manager.update_metrics("gpt-3.5-turbo", calls=1, cost=0.002)
```

To retrieve the current metrics:

```python
current_metrics = metrics_manager.get_metrics()
```

To reset all metrics:

```python
metrics_manager.reset_metrics()
```
