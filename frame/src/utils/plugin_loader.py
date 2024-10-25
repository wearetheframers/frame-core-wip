import os
import importlib
import logging
from typing import Dict, Any, List, Tuple, Optional
from dotenv import load_dotenv
import json
from frame.src.framer.brain.plugins import BasePlugin


class MockPlugin(BasePlugin):
    def get_actions(self):
        return {}


logger = logging.getLogger(__name__)


def load_plugins(plugins_dir: Optional[str] = None) -> Tuple[Dict[str, Any], List[str]]:
    """
    Load all plugins from the specified directory.

    This function scans the given directory for plugin modules, loads them,
    and returns a dictionary of plugin names and their corresponding classes.
    It also checks for conflicting action names across plugins and handles them.

    Args:
        plugins_dir (str): The directory containing the plugins.

    Returns:
        Tuple[Dict[str, Any], List[str]]: A tuple containing:
            - A dictionary of loaded plugins, where the key is the plugin name
              and the value is the plugin class.
            - A list of warning messages for conflicting actions.
    """
    # Load environment variables from .env file
    load_dotenv()

    plugins = {}
    loaded_actions = {}
    conflict_warnings = []

    if plugins_dir is None:
        plugins_dir = os.getenv("DEFAULT_PLUGINS_DIR", "plugins")

    for item in os.listdir(plugins_dir):
        plugin_dir = os.path.join(plugins_dir, item)
        print("DA PLUGIN DIR: ", plugin_dir)
        if os.path.isdir(plugin_dir) and not item.startswith("_"):
            try:
                # Load plugin-specific configuration
                config = load_plugin_config(plugin_dir)

                # Import the plugin module
                logger.debug(f"Attempting to import module for plugin: plugins.{plugin_dir}")
                module = importlib.import_module(f"plugins.{item}.{item}")
                logger.info(f"Module imported successfully for plugin: {plugin_dir}")

                # Construct the plugin class name by converting the directory name to CamelCase
                plugin_class_name = "".join(
                    word.capitalize() for word in item.split("_")
                )
                logger.debug(f"Looking for class {plugin_class_name} in module {item}")
                plugin_class = getattr(module, plugin_class_name, None)
                if plugin_class is None:
                    logger.warning(
                        f"Class {plugin_class_name} not found in module {item}. Skipping."
                    )
                    continue

                # Check if the plugin class inherits from PluginBase
                if not issubclass(plugin_class, BasePlugin):
                    logger.warning(
                        f"Plugin {item} does not inherit from PluginBase. Skipping."
                    )
                    continue

                # Check if the plugin is a default plugin or included in permissions
                permission_name = f"with_{item}"
                if item in os.getenv("DEFAULT_PLUGINS", "").split(",") or permission_name in os.getenv("PERMISSIONS", "").split(","):
                    # Check if the plugin is a default plugin or included in permissions
                    permission_name = f"with_{item}"
                    if item in os.getenv("DEFAULT_PLUGINS", "").split(",") or permission_name in os.getenv("PERMISSIONS", "").split(","):
                        # Initialize the plugin with its configuration
                        logger.debug(f"Initializing plugin {item} with configuration")
                        plugin_instance = plugin_class(config)

                        # Check for conflicting actions
                        plugin_actions = plugin_instance.get_actions()
                        for action_name, action_func in plugin_actions.items():
                            if action_name in loaded_actions:
                                conflict_warnings.append(
                                    f"Action '{action_name}' in plugin '{item}' conflicts with an existing action. Skipping."
                                )
                            else:
                                loaded_actions[action_name] = action_func

                        # Add the plugin to the plugins dictionary
                        plugins[item] = plugin_instance
                        logger.info(f"Loaded plugin: {item}")
                    else:
                        logger.info(f"Plugin {item} not loaded due to missing permission or not being a default plugin.")
                else:
                    logger.info(f"Plugin {item} not loaded due to missing permission or not being a default plugin.")
            except (ImportError, AttributeError) as e:
                logger.error(f"Failed to load plugin {item}: {str(e)}", exc_info=True)

    for warning in conflict_warnings:
        logger.warning(warning)
    return plugins, conflict_warnings


def load_plugin_config(plugin_dir: str) -> Dict[str, Any]:
    """
    Load configuration for a specific plugin.

    This function attempts to load configuration from environment variables first,
    then falls back to a config.json file in the plugin directory if it exists.

    Args:
        plugin_dir (str): The directory of the specific plugin.

    Returns:
        Dict[str, Any]: A dictionary containing the plugin's configuration.
    """
    config = {}

    # Try to load from config.json
    config_file = os.path.join(plugin_dir, "config.json")
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            config = json.load(f)

    # Override with environment variables if they exist
    for key in config.keys():
        env_value = os.getenv(key.upper())
        if env_value is not None:
            config[key] = env_value

    return config
