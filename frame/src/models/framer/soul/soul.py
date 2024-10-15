from pydantic import BaseModel, Field, validator
from typing import Dict, Any, Union


class Soul(BaseModel):
    essence: str = Field(
        default="You are a helpful AI assistant.",
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
    seed: Dict[str, Any] = Field(
        default_factory=lambda: {"text": "You are a helpful AI assistant."},
        description="The seed for the Soul's initialization.",
    )

    class Config:
        arbitrary_types_allowed = True

    @validator("seed", pre=True, always=True)
    def process_seed(cls, v, values):
        if isinstance(v, str):
            values["essence"] = v
            return {"text": v}
        elif isinstance(v, dict):
            values["essence"] = v.get("text", v.get("essence", values.get("essence")))
            seed = {"text": values["essence"]}
            values["notes"].update(
                {k: v for k, v in v.items() if k not in ["text", "essence"]}
            )
            return seed
        elif v is None:
            return {"text": values.get("essence", "You are a helpful AI assistant.")}
        else:
            raise ValueError("Seed must be either a string, dictionary, or None.")

    @classmethod
    def from_seed(cls, seed: Union[str, Dict[str, Any]]) -> "Soul":
        """
        Create a Soul instance from a seed.

        Args:
            seed (Union[str, Dict[str, Any]]): The seed for the Soul.
                Can be either a string or a dictionary:
                - If a string is provided, it will be used as the 'essence' of the Soul.
                - If a dictionary is provided, it can include 'text' or 'essence' and other key-value pairs for notes.

        Returns:
            Soul: A new Soul instance initialized with the provided seed.
        """
        return cls(seed=seed)
