import pytest
import asyncio
import logging
from unittest.mock import Mock, patch, AsyncMock
from frame.sync_frame import SyncFrame
from frame.frame import Frame
from frame.src.services import ExecutionContext

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@pytest.fixture
def mock_async_frame():
    with patch("frame.sync_frame.SyncFrame") as mock_frame:
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
    llm_service = Mock()
    sync_frame = SyncFrame(llm_service=llm_service)
    assert isinstance(sync_frame.async_frame, Frame)


@pytest.mark.asyncio
async def test_create_framer_with_config(mock_async_frame):
    llm_service = Mock()
    sync_frame = SyncFrame(llm_service=llm_service)
    config = {"name": "test_framer", "default_model": "gpt-4o-mini"}

    mock_async_frame.create_framer.return_value = "mocked_framer"

    result = await sync_frame.create_framer(config=config)

    mock_async_frame.create_framer.assert_called_once_with(config=config)
    assert result == "mocked_framer"


@pytest.mark.asyncio
async def test_perform_task_with_result(mock_async_frame):
    llm_service = Mock()
    sync_frame = SyncFrame(llm_service=llm_service)
    mock_framer = AsyncMock()
    task = {"description": "test_task"}

    mock_framer.perform_task.return_value = {"output": "task_result"}

    result = await sync_frame.perform_task(mock_framer, task)

    mock_framer.perform_task.assert_called_once_with(task)
    assert result == {"output": "task_result"}


@pytest.mark.asyncio
async def test_process_perception(mock_async_frame):
    llm_service = Mock()
    sync_frame = SyncFrame(llm_service=llm_service)
    mock_framer = AsyncMock()
    perception = {"type": "hearing", "data": {"text": "Hello"}}

    mock_framer.sense.return_value = "decision_result"

    result = await sync_frame.process_perception(mock_framer, perception)

    mock_framer.sense.assert_called_once_with(perception)
    assert result == "decision_result"


def test_close_framer(mock_async_frame):
    llm_service = Mock()
    sync_frame = SyncFrame(llm_service=llm_service)
    mock_framer = Mock()

    sync_frame.close_framer(mock_framer)

    mock_framer.close.assert_called_once()
async def test_create_framer(mock_async_frame):
    llm_service = Mock()
    sync_frame = SyncFrame(llm_service=llm_service)
    kwargs = {"config": {"name": "test_framer"}}

    mock_async_frame.create_framer.return_value = "mocked_framer"

    result = await sync_frame.create_framer(**kwargs)

    mock_async_frame.create_framer.assert_called_once_with(**kwargs)
    assert result == "mocked_framer"


@pytest.mark.asyncio
async def test_perform_task(mock_async_frame):
    llm_service = Mock()
    sync_frame = SyncFrame(llm_service=llm_service)
    mock_framer = AsyncMock()
    task = {"task": "test_task"}

    mock_framer.perform_task.return_value = "task_result"

    result = await sync_frame.perform_task(mock_framer, task)

    mock_framer.perform_task.assert_called_once_with(task)
    assert result == "task_result"


def test_generate_tasks_from_perception(mock_async_frame):
    logger.info("Starting test_generate_tasks_from_perception")
    llm_service = Mock()
    sync_frame = SyncFrame(llm_service=llm_service)
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
