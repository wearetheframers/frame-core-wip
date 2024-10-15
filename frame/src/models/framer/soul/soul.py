from pydantic import BaseModel, Field
from typing import Dict, Any, Optional


class Soul(BaseModel):
    seed: Optional[Dict[str, str]] = Field(
        None,
        description="The seed for the Framer's initialization. Can be a string or a dictionary with a 'seed' key.",
    )
    state: Dict[str, Any] = Field(
        default_factory=dict, description="The state of the Soul"
    )

    """
    The Soul class represents the intrinsic characteristics and identity of a Framer.

    Characteristics can be set to arbitrary values such as 'low', 'medium', 'high', and 'extreme'.
    These characteristics influence the Soul and, consequently, the personality and behavior of the Framer,
    if personality is enabled in the Framer.

    Attributes:
        seed (Optional[str]): The seed for the Soul's initialization.
        state (Dict[str, Any]): The state of the Soul, including characteristics.
    """


from typing import Dict, Any
from pydantic import BaseModel, Field


class Soul(BaseModel):
    essence: str = Field(
        default="You are a helpful assistant.",
        description="The essence or core of the Soul.",
    )
    notes: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional notes or attributes of the Soul.",
    )
    state: Dict[str, Any] = Field(
        default_factory=dict,
        description="The current state of the Soul",
    )

    class Config:
        arbitrary_types_allowed = True
