from enum import IntEnum
from typing import Union
from typing import Union


"""
Priority levels and their meanings:
1. LOWEST: Minimal urgency, can be deferred indefinitely.
2. VERY_LOW: Very low urgency, can be deferred for a long time.
3. LOW: Low urgency, can be deferred.
4. MEDIUM_LOW: Slightly below average urgency.
5. MEDIUM: Average urgency, requires attention.
6. MEDIUM_HIGH: Above average urgency, should be addressed soon.
7. HIGH: High urgency, requires prompt attention.
8. VERY_HIGH: Very high urgency, requires immediate attention.
9. HIGHEST: Extremely high urgency, requires immediate action.
10. CRITICAL: Maximum urgency, critical action needed immediately.
"""


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
    def from_string(cls, value: Union[str, int]) -> "Priority":
        if isinstance(value, int):
            return cls(min(max(value, 1), 10))
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

    @classmethod
    def get(cls, value: Union[int, str, "Priority"]) -> "Priority":
        return cls.from_value(value)
