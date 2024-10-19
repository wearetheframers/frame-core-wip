from typing import Dict, Any, Callable
from .actions import CreateNewAgentAction
from .actions import GenerateRolesAndGoalsAction
from .actions import ResearchAction
from .actions import RespondAction
from .actions import ThinkAction
from .actions import ObserveAction

from typing import List

VALID_ACTIONS = [
    CreateNewAgentAction,
    GenerateRolesAndGoalsAction,
    ObserveAction,
    RespondAction,
    ThinkAction,
    ResearchAction,
]

def extend_valid_actions(new_actions: List[str]) -> None:
    """
    Extend the VALID_ACTIONS dictionary with new actions.

    Args:
        new_actions (List[str]): A list of new actions to add.
    """
    VALID_ACTIONS.extend(new_actions)

