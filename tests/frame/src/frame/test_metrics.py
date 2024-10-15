import pytest
from frame.frame import Frame
from frame.src.utils.metrics import MetricsManager
from frame.src.framer.agency.execution_context import ExecutionContext


@pytest.fixture
def frame():
    return Frame()


@pytest.mark.asyncio
async def test_metrics_tracking(frame):
    # Reset metrics using MetricsManager
    metrics_manager = MetricsManager()
    metrics_manager._metrics.clear()

    # Perform some completions
    await frame.get_completion("Test prompt 1")
    await frame.get_completion("Test prompt 2")
    await frame.get_completion("Test prompt 3", model="gpt-4")

    # Get metrics using MetricsManager
    metrics = metrics_manager.get_metrics()

    # Check total calls
    assert (
        metrics["total_calls"] >= 3
    ), f"Expected at least 3 calls, got {metrics['total_calls']}. Metrics: {metrics}"

    # Check model-specific calls
    assert metrics["models"]["gpt-3.5-turbo"]["calls"] == 2
    assert metrics["models"]["gpt-4"]["calls"] == 1

    # Check if costs are being tracked (actual values will depend on your implementation)
    assert metrics["total_cost"] > 0
    assert metrics["models"]["gpt-3.5-turbo"]["cost"] > 0
    assert metrics["models"]["gpt-4"]["cost"] > 0


def test_metrics_manager_singleton():
    # Create two instances of MetricsManager
    instance1 = MetricsManager()
    instance2 = MetricsManager()

    # Check if both instances are the same
    assert instance1 is instance2, "MetricsManager is not a singleton"

    # Check if the metrics dictionary is shared
    instance1.update_metrics("test_model", 1, 0.5)
    assert instance2.get_metrics()["models"]["test_model"]["calls"] == 1
    assert instance2.get_metrics()["models"]["test_model"]["cost"] == 0.5
