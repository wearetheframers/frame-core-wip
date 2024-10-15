from typing import Dict, Any

# Import Framer within the function to avoid circular import
# Import FramerFactory within the function to avoid circular import
from frame.src.framer.config import FramerConfig
from frame.src.services.llm.main import LLMService


def create_new_agent(self, config: Dict[str, Any]) -> Any:
    from frame.src.framer.framer_factory import FramerFactory
    from frame.src.framer.framer import Framer

    """
    Create a new agent with the required properties.

    Args:
        framer (Framer): The current Framer instance.
        config (Dict[str, Any]): Configuration for the new agent.

    Returns:
        Framer: The newly created Framer instance.
    """
    llm_service = self.llm_service
    new_config = FramerConfig(**config)
    framer_factory = FramerFactory(new_config, llm_service)
    new_framer = framer_factory.create_framer()
    return new_framer
