from typing import List, Dict, Any, Optional


class LocalContext:
    """
    Local Context Service Module

    This module provides the LocalContext class, which manages local context
    for agent components, allowing them to share information with each other.
    It serves as a base class for more specialized local contexts.
    """

    def __init__(self, soul: Optional[Any] = None, **kwargs):
        """
        Initialize the Context.

        Args:
            soul (Optional[Any]): The soul attribute for the context.
        """
        self._data = {
            "soul": soul,
            "state": kwargs,
            "history": [],
            "roles": [],
            "goals": [],
        }
        for key, value in kwargs.items():
            self._data[key] = value

    def add_to_history(self, entry: str):
        """
        Add an entry to the history.

        Args:
            entry (str): The entry to add to the history.
        """
        self._data["history"].append(entry)

    def __setattr__(self, name, value):
        if name.startswith("_"):
            super().__setattr__(name, value)
        else:
            self._data[name] = value

    def __getattr__(self, name):
        if name in self._data:
            return self._data[name]
        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{name}'"
        )

    def get(self, key, default=None):
        return self._data.get(key, default)

    def get_roles(self) -> List[Dict[str, Any]]:
        return self._data["roles"]

    def set_roles(self, roles: List[Dict[str, Any]]) -> None:
        self._data["roles"] = roles

    def get_goals(self) -> List[Dict[str, Any]]:
        return self._data["goals"]

    def set_goals(self, goals: List[Dict[str, Any]]) -> None:
        self._data["goals"] = goals

    def set_soul(self, soul: Any) -> None:
        """
        Set the soul for the context.

        Args:
            soul (Any): The soul to set.
        """
        self._data["soul"] = soul
