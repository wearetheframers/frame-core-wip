from typing import Dict, Any
from collections import defaultdict
import threading
from typing import Type


class SingletonMeta(type):
    _instances: Dict[Type, Any] = {}
    _lock: threading.Lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                cls._instances[cls] = super(SingletonMeta, cls).__call__(
                    *args, **kwargs
                )
        return cls._instances[cls]


class MetricsManager(metaclass=SingletonMeta):
    def __init__(self):
        if not hasattr(self, "_initialized"):
            self._metrics = defaultdict(lambda: {"calls": 0, "cost": 0.0})
            self._total_calls = 0
            self._total_cost = 0.0
            self._initialized = True

    def update_metrics(self, model: str, calls: int = 1, cost: float = 0.0):
        self._metrics[model]["calls"] += calls
        self._metrics[model]["cost"] += cost
        self._total_calls += calls
        self._total_cost += cost

    def get_metrics(self) -> Dict[str, Any]:
        return {
            "total_calls": self._total_calls,
            "total_cost": self._total_cost,
            "models": dict(self._metrics),
        }

    def reset_metrics(self):
        self._metrics.clear()
        self._total_calls = 0
        self._total_cost = 0.0

    def clear(self):
        self.reset_metrics()
