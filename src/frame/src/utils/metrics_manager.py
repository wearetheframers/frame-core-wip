from typing import Union


class MetricsManager:
    _instance = None
    _metrics = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MetricsManager, cls).__new__(cls)
            cls._instance._metrics = {"total_calls": 0, "models": {}}
        return cls._instance

    @classmethod
    def update_metric(
        cls, metric_name: str, value: Union[int, float, str], model: str = None
    ):
        if model:
            if model not in cls._metrics["models"]:
                cls._metrics["models"][model] = {"calls": 0, "cost": 0.0}
            if metric_name == "calls":
                cls._metrics["models"][model]["calls"] += value
            elif metric_name == "cost":
                cls._metrics["models"][model]["cost"] += value

        if metric_name not in cls._metrics:
            cls._metrics[metric_name] = value
        elif isinstance(cls._metrics[metric_name], (int, float)):
            cls._metrics[metric_name] += value
        else:
            cls._metrics[metric_name] = value

        cls._metrics["total_calls"] += 1

    @classmethod
    def get_metrics(cls):
        return cls._metrics
