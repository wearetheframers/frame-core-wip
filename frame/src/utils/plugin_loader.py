import os
import importlib
import logging
from typing import Dict, Any
from dotenv import load_dotenv
import json
from frame.src.framer.brain.plugins import PluginBase

logger = logging.getLogger(__name__)

def load_plugins(plugins_dir: str) -> Dict[str, Any]:
    """
    Load all plugins from the specified directory.

    This function scans the given directory for plugin modules, loads them,
    and returns a dictionary of plugin names and their corresponding classes.

    Args:
        plugins_dir (str): The directory containing the plugins.

    Returns:
        Dict[str, Any]: A dictionary of loaded plugins, where the key is the plugin name
                        and the value is the plugin class.
    """
    # Load environment variables from .env file
    load_dotenv()

    plugins = {}
    for item in os.listdir(plugins_dir):
        plugin_dir = os.path.join(plugins_dir, item)
        if os.path.isdir(plugin_dir) and not item.startswith('__'):
            try:
                # Load plugin-specific configuration
                config = load_plugin_config(plugin_dir)

                # Import the plugin module
                module = importlib.import_module(f"frame.src.plugins.{item}")
                plugin_class = getattr(module, f"{item.capitalize()}Plugin")

                # Check if the plugin class inherits from PluginBase
                if not issubclass(plugin_class, PluginBase):
                    logger.warning(f"Plugin {item} does not inherit from PluginBase. Skipping.")
                    continue

                # Initialize the plugin with its configuration
                plugins[item] = plugin_class(config)
                logger.info(f"Loaded plugin: {item}")
            except (ImportError, AttributeError) as e:
                logger.warning(f"Failed to load plugin {item}: {str(e)}")
    return plugins

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
    config_file = os.path.join(plugin_dir, 'config.json')
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            config = json.load(f)

    # Override with environment variables if they exist
    for key in config.keys():
        env_value = os.getenv(key.upper())
        if env_value is not None:
            config[key] = env_value

    return config
