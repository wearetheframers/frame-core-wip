import pytest
import asyncio
import logging
from unittest.mock import Mock, patch, AsyncMock
from frame.sync_frame import SyncFrame, sync_frame
from frame.frame import Frame
from frame.src.framer.agency.execution_context import ExecutionContext

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@pytest.fixture
def mock_async_frame():
    with patch("frame.sync_frame.Frame") as mock_frame:
        mock_frame.return_value = AsyncMock()
        yield mock_frame.return_value


@pytest.fixture(autouse=True)
def cleanup():
    yield
    if hasattr(sync_frame, "close"):
        sync_frame.close()


@pytest.fixture(autouse=True)
def debug_test(request):
    logger.info(f"Starting test: {request.node.name}")
    yield
    logger.info(f"Finished test: {request.node.name}")


def test_sync_frame_initialization():
    sync_frame = SyncFrame()
    assert isinstance(sync_frame.async_frame, Frame)


@pytest.mark.asyncio
async def test_create_framer(mock_async_frame):
    sync_frame = SyncFrame()
    kwargs = {"config": {"name": "test_framer"}}

    mock_async_frame.create_framer.return_value = "mocked_framer"

    result = await sync_frame.create_framer(**kwargs)

    mock_async_frame.create_framer.assert_called_once_with(**kwargs)
    assert result == "mocked_framer"


@pytest.mark.asyncio
async def test_perform_task(mock_async_frame):
    sync_frame = SyncFrame()
    mock_framer = AsyncMock()
    task = {"task": "test_task"}

    mock_framer.perform_task.return_value = "task_result"

    result = await sync_frame.perform_task(mock_framer, task)

    mock_framer.perform_task.assert_called_once_with(task)
    assert result == "task_result"


def test_generate_tasks_from_perception(mock_async_frame):
    logger.info("Starting test_generate_tasks_from_perception")
    sync_frame = SyncFrame()
    mock_framer = AsyncMock()
    perception = {"perception": "test_perception"}

    async def mock_generate_tasks(*args, **kwargs):
        logger.info("Mock generate_tasks_from_perception called")
        await asyncio.sleep(0.1)  # Simulate some work
        return ["task1", "task2"]

    mock_framer.generate_tasks_from_perception.side_effect = mock_generate_tasks

    logger.info("Calling generate_tasks_from_perception")
    result = sync_frame.generate_tasks_from_perception(
        mock_framer, perception, max_len=2048, timeout=5
    )
    logger.info(f"Result: {result}")

    mock_framer.generate_tasks_from_perception.assert_called_once_with(
        perception, max_len=2048
    )
    assert result == ["task1", "task2"]
    logger.info("test_generate_tasks_from_perception completed")


@pytest.mark.asyncio
async def test_sense(mock_async_frame):
    sync_frame = SyncFrame()
    mock_framer = AsyncMock()
    perception = {"perception": "test_perception"}

    mock_framer.sense = AsyncMock(return_value="sense_result")

    result = await sync_frame.sense(mock_framer, perception)

    mock_framer.sense.assert_called_once_with(perception)
    assert result == "sense_result"


def test_sync_frame_singleton():
    assert isinstance(sync_frame, SyncFrame)
