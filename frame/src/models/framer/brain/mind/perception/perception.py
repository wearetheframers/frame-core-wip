from pydantic import BaseModel, Field, ConfigDict, root_validator
from typing import Any, Dict, Optional, Union
from datetime import datetime


class Perception(BaseModel):
    type: str = Field(..., description="The type of perception")
    data: Dict[str, Any] = Field(
        ..., description="The data associated with the perception"
    )
    source: Optional[str] = Field(None, description="The source of the perception")
    timestamp: datetime = Field(
        default_factory=datetime.now,
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
