"""
Common utilities for the Frame CLI.

This module provides common functions and utilities used across the Frame CLI
commands, including logging, role and goal generation, and perception processing.

Attributes:
    logger (Logger): Logger instance for logging common activities.
"""

import logging
from typing import Any, Dict, List, Optional
from frame.src.constants.models import DEFAULT_MODEL
from frame.src.framer.config import FramerConfig
from frame.src.framer.framer_factory import FramerFactory
from frame.src.framer.agency import Agency
from frame.src.services.context.context_service import Context
from frame.src.framer.framer import Framer
from frame.frame import Frame
from frame.src.framer.brain.decision import Decision
from frame.src.framer.soul.soul import Soul

logger = logging.getLogger(__name__)


def execute_framer(
    framer: Framer, action: str, parameters: Optional[Dict[str, Any]] = None
) -> None:
    """
    Execute a specified action on the Framer.

    Args:
        framer (Framer): The Framer instance to execute the action on.
        action (str): The action to execute.
        parameters (Optional[Dict[str, Any]]): Parameters for the action.
    """
    logger.info(f"Executing action '{action}' with parameters: {parameters}")
    # Placeholder for actual execution logic
    # This should be replaced with the actual implementation
    pass


def pretty_log(obj: Any) -> str:
    """
    Convert an object to a pretty string for logging.

    Args:
        obj (Any): The object to convert.

    Returns:
        str: A formatted string representation of the object.
    """
    if isinstance(obj, dict):
        return "\n" + "\n".join(f"  {k}: {v}" for k, v in obj.items())
    elif isinstance(obj, list):
        return "\n" + "\n".join(f"  - {item}" for item in obj)
    else:
        return str(obj)


async def generate_roles_and_goals(framer: Framer, prompt: str) -> None:
    """
    Generate roles and goals for a Framer based on a prompt.

    This function uses the Framer's language model service to generate roles
    and goals from a given prompt and updates the Framer's configuration.

    Args:
        framer (Framer): The Framer instance to update.
        prompt (str): The prompt to generate roles and goals from.
    """
    logger.debug(f"Generating roles and goals for prompt: {prompt}")
    logger.debug(f"Framer brain before generating roles and goals: {framer.brain}")

    if framer.brain is None:
        logger.error("Framer brain is None before generating roles and goals")
        raise ValueError("Framer brain is not initialized")

    # Generate roles and goals
    roles, goals = await framer.agency.generate_roles_and_goals()

    logger.info(f"Generated roles: {pretty_log(roles)}")
    logger.info(f"Generated goals: {pretty_log(goals)}")

    framer.agency.set_roles(roles)
    framer.agency.set_goals(goals)

    if framer.brain is None:
        logger.error("Framer brain is None after generating roles and goals")
        raise ValueError("Framer brain became None during role and goal generation")


async def process_perception_and_log(
    framer: Framer, perception: Dict[str, Any]
) -> Decision:
    """
    Process a perception and log the resulting decision.

    This function processes a perception using the Framer's sense method and
    logs the resulting decision.

    Args:
        framer (Framer): The Framer instance to use.
        perception (Dict[str, Any]): The perception data to process.

    Returns:
        Decision: The decision made based on the perception.
    """
    logger.debug(f"Processing perception: {perception}")
    decision = await framer.sense(perception)
    logger.info(f"Decision: {pretty_log(decision)}")
    return decision


async def setup_framer(
    frame: Frame, name: str, description: str, model: str, soul_seed: str
) -> Framer:
    """
    Set up a Framer instance with the given configuration.

    This function initializes a Framer with the specified name, description,
    model, and soul seed, and sets up its agency and context.

    Args:
        frame (Frame): Frame instance for managing Framer operations.
        name (str): Name of the Framer.
        description (str): Description of the Framer's purpose.
        model (str): AI model to use for the Framer.
        soul_seed (str): Seed phrase to initialize the Framer's soul.

    Returns:
        Framer: The initialized Framer instance.
    """
    config = FramerConfig(
        name=name,
        description=description,
        default_model=model.lower(),
    )
    framer_factory = FramerFactory(config, frame.llm_service, roles=roles, goals=goals)
    framer = await framer_factory.create_framer()
    logger.debug(f"Framer brain after build: {framer.brain}")

    if framer.soul is None:
        logger.warning("Framer's Soul is null. Initializing with default values.")
        framer.soul = Soul(seed=config.soul_seed)
    else:
        framer.soul.seed = config.soul_seed  # Explicitly set the soul seed

    context: Dict[str, Any] = {}
    framer.agency = Agency(
        llm_service=frame.llm_service,
        context=context,
    )
    logger.info(f"Using model: {model}")
    return framer
