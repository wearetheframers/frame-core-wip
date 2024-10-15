from pydantic import BaseModel, Field, ConfigDict, root_validator
from typing import Any, Dict, Optional
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
        arbitrary_types_allowed = True
