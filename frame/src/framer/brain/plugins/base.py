from abc import ABC, abstractmethod
from typing import Any, Dict
from frame.src.framer.agency.priority import Priority


class BasePlugin(ABC):
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

    def remove_action(self, name: str):
        """
        Remove an action from the action registry by its name.

        Args:
            name (str): The name of the action to remove.
        """
        if name in self.framer.brain.action_registry.actions:
            # del self.framer.brain.action_registry.actions[name]
            self.framer.brain.action_registry.remove_action(name)
            print(f"Action '{name}' removed from registry.")
        else:
            print(f"Action '{name}' not found in registry.")

    @abstractmethod
    async def on_load(self):
        """
        Abstract method that is called when the plugin is loaded.

        This method should be implemented by all plugin subclasses to perform
        any necessary initialization or setup when the plugin is loaded.
        """
        pass

    def add_action(self, name: str, func: callable, description: str, priority: Priority = Priority.MEDIUM):
        """
        Register an action with the Framer's action registry.

        This method allows the plugin to add new actions that can be performed by the Framer.

        Args:
            name (str): The name of the action.
            func (callable): The function to be called when the action is performed.
            description (str): A brief description of what the action does.
        """
        print("Registering action: ", name)
        if name not in self.framer.brain.action_registry.actions:
            self.framer.brain.action_registry.add_action(name, func, description, priority)
            print(f"Action '{name}' registered to Framer action registry.")
        else:
            print(f"Action '{name}' already exists in Framer action registry.")

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


# This file serves as a reference for plugin developers.
# Actual plugins should be implemented in separate files,
# inheriting from the PluginBase class.


class ExamplePlugin(BasePlugin):
    async def on_load(self):
        self.logger.info("Example plugin loaded")
        # Example of using get_api_key method
        try:
            api_key = self.get_api_key("EXAMPLE_API_KEY")
            self.logger.info(f"API key retrieved: {api_key[:5]}...")
        except ValueError as e:
            self.logger.warning(f"API key not found: {e}")

    async def on_unload(self):
        self.logger.info("Example plugin unloaded")

    async def on_decision_made(self, decision):
        self.logger.info(f"Decision made: {decision}")


# Note: This is just an example. Don't instantiate plugins here.
# Plugins should be instantiated and registered by the Framer.
