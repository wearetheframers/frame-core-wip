from abc import ABC, abstractmethod
import logging
import os
import json
from typing import Any, Dict, Callable
from frame.src.framer.agency.priority import Priority
from frame.src.framer.brain.rules.ruleset import Rule, Ruleset


class BasePlugin(ABC):
    def __init__(self, framer):
        self.framer = framer
        self.logger = logging.getLogger(self.__class__.__name__)
        self.execution_context = getattr(framer, "execution_context", None)
        self.ruleset = Ruleset()

    def load_config(self, plugin_dir: str) -> Dict[str, Any]:
        """
        Load configuration for the plugin, prioritizing environment variables,
        then .env file, and finally config.json in the plugin directory.

        Args:
            plugin_dir (str): The directory of the plugin.

        Returns:
            Dict[str, Any]: The loaded configuration.
        """
        config = {}

        # Load from config.json
        config_file = os.path.join(plugin_dir, "config.json")
        if os.path.exists(config_file):
            with open(config_file, "r") as f:
                config = json.load(f)

        # Override with environment variables
        for key in config.keys():
            env_value = os.getenv(key.upper())
            if env_value is not None:
                config[key] = env_value

        return config

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
        self.logger = logging.getLogger(self.__class__.__name__)
        self.execution_context = getattr(framer, "execution_context", None)
        self.ruleset = Ruleset()
        self.logger.warning(
            "Plugin warning: Framer does not have an execution_context attribute. Possible unexpected behaviors may occur."
        )

    def add_rule(
        self,
        condition: Callable[[Dict[str, Any]], bool],
        action: Callable[[Dict[str, Any]], None],
    ):
        """
        Add a rule to the plugin.

        Args:
            condition (Callable[[Dict[str, Any]], bool]): The condition function for the rule.
            action (Callable[[Dict[str, Any]], None]): The action function to execute if the condition is met.
        """
        rule = Rule(condition, action)
        self.ruleset.add_rule(rule)

    @abstractmethod
    async def on_load(self):
        """
        Abstract method that is called when the plugin is loaded.

        This method should be implemented by all plugin subclasses to perform
        any necessary initialization or setup when the plugin is loaded.
        """
        pass

    def add_action(
        self,
        name: str,
        action_func: callable,
        description: str,
        priority: Priority = Priority.MEDIUM,
    ):
        """
        Register an action with the Framer's action registry.

        This method allows the plugin to add new actions that can be performed by the Framer.

        Args:
            name (str): The name of the action.
            func (callable): The function to be called when the action is performed.
            description (str): A brief description of what the action does.
        """
        if name not in self.framer.brain.action_registry.actions:
            self.framer.brain.action_registry.add_action(
                name, action_func, description, priority
            )
            self.logger.warning(
                f"Action '{name}' registered in Framer action registry."
            )
        else:
            self.logger.warning(
                f"Action '{name}' already exists in Framer action registry."
            )

    @abstractmethod
    @abstractmethod
    async def on_remove(self):
        """
        Abstract method that is called when the plugin is removed.

        This method should be implemented by all plugin subclasses to perform
        any necessary cleanup or teardown when the plugin is removed.
        """
        pass

    async def execute(self, action: str, params: Dict[str, Any], execution_context: Any) -> Any:
        """
        Execute a plugin action.

        :param action: The name of the action to execute.
        :param params: A dictionary of parameters for the action.
        :param execution_context: The context in which the action is executed.
        :return: The result of the action.
        """
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

    def get_actions(self):
        return {}

    async def on_decision_made(self, decision):
        self.logger.info(f"Decision made: {decision}")


# Note: This is just an example. Don't instantiate plugins here.
# Plugins should be instantiated and registered by the Framer.
class BasePlugin:
    def __init__(self, framer):
        self.framer = framer
        self.actions = {}

    def get_actions(self):
        """
        Return the actions registered by this plugin.
        """
        return self.actions

    def add_action(self, name, action_func, description=""):
        """
        Add an action to the plugin's action registry.

        Args:
            name (str): The name of the action.
            action_func (callable): The function to execute for this action.
            description (str): A description of the action.
        """
        self.actions[name] = {
            "action_func": action_func,
            "description": description,
        }
