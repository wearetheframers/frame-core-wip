from typing import Any, Dict, List
import logging


class LoggingMixin:
    """
    A mixin that provides logging capabilities to a class.

    This mixin initializes a logger for the class and provides a method
    to log messages at different levels.
    """

    def __init__(self, *args, **kwargs):
        self.logger = logging.getLogger(self.__class__.__name__)

    def log(self, message: str, level: str = "info") -> None:
        getattr(self.logger, level)(f"{self.__class__.__name__}: {message}")


class ConfigurableMixin:
    """
    A mixin that provides configuration management capabilities to a class.

    This mixin allows a class to store and retrieve configuration settings
    using a dictionary. It provides methods to get and set configuration
    values.
    """

    def __init__(self, *args, **kwargs):
        self.config: Dict[str, Any] = kwargs.get("config", {})

    def get_config(self, key: str, default: Any = None) -> Any:
        return self.config.get(key, default)

    def set_config(self, key: str, value: Any) -> None:
        self.config[key] = value


class MetricsMixin:
    """
    A mixin that provides metrics recording capabilities to a class.

    This mixin allows a class to record and retrieve metrics using a dictionary.
    It provides methods to record a metric, get a specific metric, and retrieve
    all recorded metrics.
    """

    def __init__(self, *args, **kwargs):
        self.metrics: Dict[str, Any] = {}

    def record_metric(self, key: str, value: Any) -> None:
        self.metrics[key] = value

    def get_metric(self, key: str) -> Any:
        return self.metrics.get(key)

    def get_all_metrics(self) -> Dict[str, Any]:
        return self.metrics
