from typing import Dict, Any, Callable
"""
Default Actions

This module defines the default actions available in the Frame framework. It includes high-level actions like
AdaptiveDecisionAction and CreateNewAgentAction, which are designed to manage complex tasks by leveraging
multiple strategies or sub-actions.
"""

from frame.src.framer.brain.actions import CreateNewAgentAction, AdaptiveDecisionAction
from frame.src.framer.brain.actions import GenerateRolesAndGoalsAction
from frame.src.framer.brain.actions import ResearchAction
from frame.src.framer.brain.actions import RespondAction
from frame.src.framer.brain.actions import ThinkAction
from frame.src.framer.brain.actions import ObserveAction

from typing import List

DEFAULT_ACTIONS = [
    CreateNewAgentAction,
    GenerateRolesAndGoalsAction,
    ObserveAction,
    RespondAction,
    ThinkAction,
    ResearchAction,
    AdaptiveDecisionAction,
]


def extend_default_actions(new_actions: List[str]) -> None:
    """
    Extend the DEFAULT_ACTIONS dictionary with new actions.

    Args:
        new_actions (List[str]): A list of new actions to add.
    """
    DEFAULT_ACTIONS.extend(new_actions)
