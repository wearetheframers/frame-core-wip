import pytest
from frame.src.framer.brain.perception.perception import Perception
from frame.src.models.framer.brain.mind.perception import Perception as PerceptionModel
from datetime import datetime, timezone


def test_perception_initialization():
    perception = Perception(type="test", data={"key": "value"}, source="test_source")
    assert isinstance(perception, Perception)
    assert isinstance(perception, PerceptionModel)
    assert perception.type == "test"
    assert perception.data == {"key": "value"}
    assert perception.source == "test_source"
    assert isinstance(perception.timestamp, datetime)


def test_perception_to_dict():
    perception = Perception(type="test", data={"key": "value"}, source="test_source")
    perception_dict = perception.to_dict()
    assert isinstance(perception_dict, dict)
    assert perception_dict["type"] == "test"
    assert perception_dict["data"] == {"key": "value"}
    assert perception_dict["source"] == "test_source"
    assert isinstance(perception_dict["timestamp"], str)


def test_perception_from_dict():
    current_time = datetime.now(timezone.utc)
    perception_dict = {
        "type": "test",
        "data": {"key": "value"},
        "source": "test_source",
        "timestamp": current_time.isoformat(),
    }
    perception = Perception.from_dict(perception_dict)
    assert isinstance(perception, Perception)
    assert perception.type == "test"
    assert perception.data == {"key": "value"}
    assert perception.source == "test_source"
    assert perception.timestamp == current_time


def test_perception_from_dict_without_source():
    current_time = datetime.now(timezone.utc)
    perception_dict = {
        "type": "test",
        "data": {"key": "value"},
        "timestamp": current_time.isoformat(),
    }
    perception = Perception.from_dict(perception_dict)
    assert isinstance(perception, Perception)
    assert perception.type == "test"
    assert perception.data == {"key": "value"}
    assert perception.source is None
    assert perception.timestamp == current_time


def test_perception_from_dict_without_timestamp():
    perception_dict = {
        "type": "test",
        "data": {"key": "value"},
        "source": "test_source",
    }
    perception = Perception.from_dict(perception_dict)
    assert isinstance(perception, Perception)
    assert perception.type == "test"
    assert perception.data == {"key": "value"}
    assert perception.source == "test_source"
    assert isinstance(perception.timestamp, datetime)
