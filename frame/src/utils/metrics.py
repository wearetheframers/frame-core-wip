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
            self._initialized = True

    def update_metrics(self, model: str, calls: int, cost: float):
        self._metrics[model]["calls"] += calls
        self._metrics[model]["cost"] += cost

    def get_metrics(self) -> Dict[str, Any]:
        total_calls = sum(data["calls"] for data in self._metrics.values())
        total_cost = sum(data["cost"] for data in self._metrics.values())
        return {
            "total_calls": total_calls,
            "total_cost": total_cost,
            "models": dict(self._metrics),
        }
