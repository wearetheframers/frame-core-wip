from frame.src.models.framer.brain.mind.perception.perception import (
    Perception as PerceptionModel,
)
from typing import Any, Dict, Optional, Union
from datetime import datetime


class Perception(PerceptionModel):
    """
    Represents a perception in the Frame system.
    
    Perceptions in Frame can be any type of information or stimulus, not limited to human senses.
    This includes traditional inputs like text, images, or sounds, but also extends to more abstract
    or non-human sensory data such as magnetic fields, vibrations, internal states like hunger,
    or any other data that can be analyzed by the language model.
    
    The "prompt" action in a Framer is essentially processing a perception of hearing for text input
    and responding to it.
    """

    def __init__(
        self,
        type: str,
        data: Dict[str, Any],
        source: Optional[str] = None,
        timestamp: Optional[datetime] = None,
    ):
        """
        Initialize a Perception instance.

        Args:
            type (str): The type of perception (e.g., 'visual', 'auditory', 'text', 'magnetic', 'internal_state', etc.)
            data (Dict[str, Any]): The data associated with the perception. Can contain any type of information.
            source (Optional[str]): The source of the perception (e.g., 'camera', 'microphone', 'text_input', 'magnetometer', 'internal_sensor', etc.)
            timestamp (Optional[datetime]): The timestamp of when the perception was created. If None, current time is used.
        """
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
    def from_dict(cls, perception_dict: Union[Dict[str, Any], str]) -> "Perception":
        if isinstance(perception_dict, str):
            return cls(type="hearing", data={"text": perception_dict})
        elif not isinstance(perception_dict, dict):
            raise TypeError("perception_dict must be a dictionary or a string")

        timestamp = perception_dict.get("timestamp")
        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp)

        return cls(
            type=perception_dict.get("type", "unknown"),
            data=perception_dict.get("data", {}),
            source=perception_dict.get("source"),
            timestamp=timestamp,
        )
