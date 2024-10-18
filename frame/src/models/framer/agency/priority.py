from enum import IntEnum
from typing import Union


class Priority(IntEnum):
    LOWEST = 1
    VERY_LOW = 2
    LOW = 3
    MEDIUM_LOW = 4
    MEDIUM = 5
    MEDIUM_HIGH = 6
    HIGH = 7
    VERY_HIGH = 8
    HIGHEST = 9
    CRITICAL = 10

    @classmethod
    def from_string(cls, value: str) -> "Priority":
        string_to_priority = {
            "lowest": cls.LOWEST,
            "very low": cls.VERY_LOW,
            "low": cls.LOW,
            "medium low": cls.MEDIUM_LOW,
            "medium": cls.MEDIUM,
            "medium high": cls.MEDIUM_HIGH,
            "high": cls.HIGH,
            "very high": cls.VERY_HIGH,
            "highest": cls.HIGHEST,
            "critical": cls.CRITICAL,
        }
        return string_to_priority.get(value.lower(), cls.MEDIUM)

    @classmethod
    def from_value(cls, value: Union[int, str, "Priority"]) -> "Priority":
        if isinstance(value, cls):
            return value
        elif isinstance(value, int):
            return cls(min(max(value, 1), 10))
        elif isinstance(value, str):
            return cls.from_string(value)
        else:
            raise ValueError(
                "Priority must be an integer, string, or Priority instance"
            )
