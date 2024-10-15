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


from typing import Dict, Any, Union
from pydantic import BaseModel, Field


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

    def __init__(self, **data):
        super().__init__(**data)
        if 'seed' in data:
            self._process_seed(data['seed'])
        else:
            self.seed = {"text": "You are a helpful AI assistant."}

    def _process_seed(self, seed: Union[str, Dict[str, Any]]):
        if isinstance(seed, str):
            self.essence = seed
            self.seed = {"text": seed}
        elif isinstance(seed, dict):
            self.essence = seed.get('text', seed.get('essence', self.essence))
            self.seed = {"text": self.essence}
            self.notes.update({k: v for k, v in seed.items() if k not in ['text', 'essence']})
        else:
            raise ValueError("Seed must be either a string or a dictionary.")
        
        if 'text' not in self.seed:
            self.seed['text'] = self.essence

    @classmethod
    def from_seed(cls, seed: Union[str, Dict[str, Any]]) -> 'Soul':
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
