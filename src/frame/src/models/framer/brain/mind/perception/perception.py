from pydantic import BaseModel, Field, ConfigDict, root_validator
from typing import Any, Dict, Optional, Union
from datetime import datetime


class Perception(BaseModel):
    """
    Represents a perception in the Frame system.

    Perceptions in Frame can be any type of information or stimulus, not limited to human senses.
    This includes traditional inputs like text, images, or sounds, but also extends to more abstract
    or non-human sensory data such as magnetic fields, vibrations, internal states like hunger,
    or any other data that can be analyzed by the language model.

    The "prompt" action in a Framer is essentially processing a perception of hearing for text input
    and responding to it.
    """

    type: str = Field(
        ...,
        description="The type of perception (e.g., 'visual', 'auditory', 'text', 'magnetic', 'internal_state', etc.)",
    )
    data: Dict[str, Any] = Field(
        ...,
        description="The data associated with the perception. Can contain any type of information.",
    )
    source: Optional[str] = Field(
        None,
        description="The source of the perception (e.g., 'camera', 'microphone', 'text_input', 'magnetometer', 'internal_sensor', etc.)",
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="The timestamp of when the perception was created",
    )

    @root_validator(pre=True)
    def check_data_key(cls, values):
        if "data" not in values or not isinstance(values["data"], dict):
            raise ValueError(
                "Perception data must include a 'data' key with a dictionary value."
            )
        return values

    @classmethod
    def from_dict(cls, perception_dict: Union[Dict[str, Any], str]) -> "Perception":
        if isinstance(perception_dict, str):
            return cls(type="hearing", data={"text": perception_dict})
        elif not isinstance(perception_dict, dict):
            raise TypeError("perception_dict must be a dictionary or a string")
        return cls(**perception_dict)
