from typing import Dict, Any
from frame.src.framer.config import FramerConfig


def create_new_agent(self, config: Dict[str, Any]):
    """
    Create a new agent with the required properties.

    Args:
        self: The current Framer instance.
        config (Dict[str, Any]): Configuration for the new agent.

    Returns:
        Framer: The newly created Framer instance.
    """
    new_config = FramerConfig(
        name=config.get("name", "New Framer"), model=config.get("model")
    )
    new_framer = self.create_framer(new_config)
    return new_framer
