from abc import ABC, abstractmethod
from typing import Any, Dict

class PluginBase(ABC):
    """
    Base class for all Frame plugins.

    This class defines the basic structure and interface that all plugins should follow.
    Plugins provide a way to extend the functionality of Framer instances.

    Attributes:
        framer: The Framer instance that this plugin is associated with.
    """

    def __init__(self, framer):
        """
        Initialize the plugin with a Framer instance.

        Args:
            framer: The Framer instance to associate with this plugin.
        """
        self.framer = framer

    @abstractmethod
    async def on_load(self):
        """
        Abstract method that is called when the plugin is loaded.

        This method should be implemented by all plugin subclasses to perform
        any necessary initialization or setup when the plugin is loaded.
        """
        pass

    def register_action(self, name: str, func: callable, description: str):
        """
        Register an action with the Framer's action registry.

        This method allows the plugin to add new actions that can be performed by the Framer.

        Args:
            name (str): The name of the action.
            func (callable): The function to be called when the action is performed.
            description (str): A brief description of what the action does.
        """
        self.framer.brain.action_registry.register_action(name, func, description)

    @abstractmethod
    async def execute(self, action: str, params: Dict[str, Any]) -> Any:
        """
        Abstract method to execute a plugin-specific action.

        This method should be implemented by all plugin subclasses to handle
        plugin-specific actions.

        Args:
            action (str): The name of the action to execute.
            params (Dict[str, Any]): Parameters for the action.

        Returns:
            Any: The result of the action execution.
        """
        pass
