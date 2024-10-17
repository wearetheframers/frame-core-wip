from frame.src.models.framer.brain.mind.perception import Perception as PerceptionModel
from typing import Any, Dict, Optional
from datetime import datetime


class Perception(PerceptionModel):
    def __init__(
        self,
        type: str,
        data: Dict[str, Any],
        source: Optional[str] = None,
        timestamp: Optional[datetime] = None,
    ):
        super().__init__(
            type=type,
            data=data,
            source=source,
            timestamp=timestamp or datetime.utcnow(),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type,
            "data": self.data,
            "source": self.source,
            "timestamp": self.timestamp.isoformat(),
        }

    @classmethod
    def from_dict(cls, perception_dict: Any) -> "Perception":
        if not isinstance(perception_dict, dict):
            raise TypeError("perception_dict must be a dictionary")

        timestamp = perception_dict.get("timestamp")
        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp)

        return cls(
            type=perception_dict.get("type", "unknown"),
            data=perception_dict.get("data", {}),
            source=perception_dict.get("source"),
            timestamp=timestamp,
        )
