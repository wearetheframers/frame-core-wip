from typing import Dict, Any, Optional, Union, List
from frame.src.models.framer.soul.soul import Soul as SoulModel


class Soul:
    def __init__(self, seed: Optional[Union[str, Dict[str, Any]]] = None, traits: Optional[List[str]] = None) -> None:
        """
        Initialize a Soul instance.

        Args:
            seed (Optional[Union[str, Dict[str, Any]]], optional): The initial seed for the Soul.
                Can be either a string or a dictionary:
                - If a string is provided, it will be used as the 'text' value in the soul's seed dictionary.
                - If a dictionary is provided, it can include any keys and values, with an optional 'text' key for the soul's essence.
                The 'text' key is used for the essence, and all other key-value pairs
                are stored in the notes. The values can be of any type. Defaults to None.
            traits (Optional[List[str]], optional): A list of traits for the Soul. Defaults to None.

        Raises:
            ValueError: If the seed is not a string, dictionary, or None.
        """
        self.model = SoulModel(seed=seed)
        self.seed = self.model.seed
        self.traits = traits or []

    def update_state(self, key: str, value: Any) -> None:
        """
        Update the Soul's state with new information.

        Args:
            key (str): The key to update.
            value (Any): The value to set.
        """
        self.model.state[key] = value

    def get_state(self, key: str) -> Any:
        """
        Get a value from the Soul's state.

        Args:
            key (str): The key to retrieve.

        Returns:
            Any: The value associated with the key, or None if not found.
        """
        return self.model.state.get(key)

    @property
    def state(self):
        return self.model.state

    def get_current_state(self) -> Dict[str, Any]:
        """
        Get a copy of the current state of the Soul.

        Returns:
            Dict[str, Any]: A shallow copy of the current state of the Soul.
        """
        return self.model.state.copy()

    def generate_state_summary(self) -> str:
        """
        Generate a summary of the Soul's current state.

        Returns:
            str: A string summarizing the current state of the Soul.
        """
        return f"Soul State Summary:\nEssence: {self.model.essence}\nNotes: {self.model.notes}\nCurrent state: {self.model.state}"

    def update_notes(self, key: str, value: Any) -> None:
        """
        Update the Soul's notes with new information.

        Args:
            key (str): The key to update.
            value (Any): The value to set.
        """
        self.model.notes[key] = value

    def update_essence(self, essence: str) -> None:
        """
        Update the Soul's essence.

        Args:
            essence (str): The new essence to set.
        """
        self.model.essence = essence

    def get_notes(self) -> Dict[str, Any]:
        """
        Get a copy of the current notes of the Soul model.

        Returns:
            Dict[str, Any]: A copy of the current notes.
        """
        return self.model.notes.copy()

    def get_essence(self) -> str:
        """
        Get the current essence of the Soul model.

        Returns:
            str: The current essence.
        """
        return self.model.essence

    def get_model(self) -> SoulModel:
        """
        Get the full Soul model instance.

        Returns:
            SoulModel: The full Soul model instance.
        """
        return self.model

    def reset_state(self) -> None:
        """
        Reset the Soul's state to an empty dictionary.
        """
        self.model.state = {}

    def reset_notes(self) -> None:
        """
        Reset the Soul's notes to an empty dictionary.
        """
        self.model.notes = {}

    def reset_essence(self) -> None:
        """
        Reset the Soul's essence to the default value.
        """
        self.model.essence = "You are a helpful assistant."

    def reset_model(self, seed: Dict[str, Any]) -> None:
        """
        Reset the entire Soul model with a new seed dictionary.

        Args:
            seed (Dict[str, Any]): A dictionary containing the new seed for the Soul.
        """
        self.model = SoulModel(seed=seed)

    def copy(self) -> "Soul":
        """
        Create a copy of the Soul model.

        Returns:
            Soul: A new instance of the Soul class with a copy of the current model.
        """
        return Soul(seed={"text": self.model.essence, **self.model.notes})
