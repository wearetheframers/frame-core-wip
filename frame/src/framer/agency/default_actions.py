from typing import Dict, Any, Callable
from .actions import create_new_agent
from .actions import generate_roles_and_goals
from .actions import research
from .actions import respond
from .actions import think
from .actions import observe
from .actions import observe  # Import the observe function


def extend_valid_actions(new_actions: Dict[str, Dict[str, Any]]) -> None:
    """
    Extend the VALID_ACTIONS dictionary with new actions.

    Args:
        new_actions (Dict[str, Dict[str, Any]]): A dictionary of new actions to add.
        Each action should have the following structure:
        {
            "action_name": {
                "func": Callable,
                "description": str,
                "priority": int
            }
        }
    """
    VALID_ACTIONS.update(new_actions)


VALID_ACTIONS: Dict[str, Dict[str, Any]] = {
    "create_new_agent": {
        "func": create_new_agent,
        "description": (
            "Create a new agent only when the current agent is unable or unwilling "
            "to perform the requested task. The new agent should have the required "
            "properties, such as plugins, configuration, and prompt, to accomplish the task."
        ),
        "priority": 5,
    },
    "generate_roles_and_goals": {
        "func": generate_roles_and_goals,
        "description": (
            "Generate roles and goals if the current ones are too limited, "
            "ensuring that the agent can effectively achieve its objectives."
        ),
        "priority": 5,
    },
    "research": {
        "func": research,
        "description": (
            "Perform research only if the Framer agent cannot provide enough answers on its own "
            "or if the user specifically requests it. Gather information from external sources "
            "and provide a concise summary of the findings that directly addresses the research question."
        ),
        "priority": 5,
    },
    "respond": {
        "func": respond,
        "description": (
            "Generate a response that directly addresses the given input or query, "
            "ensuring clarity and relevance in the communication."
        ),
        "priority": 5,
    },
    "think": {
        "func": think,
        "description": "Ponder and reflect on the current situation, potentially creating new tasks or generating a new prompt. Only necessary if a new prompt should be generated with new pretext and context for better results.",
        "priority": 2,
    },
    "use": {
        "func": lambda *args, **kwargs: None,
        "description": "Use a specific tool or resource to accomplish a task.",
        "priority": 5,
    },
    "observe": {
        "func": observe,
        "description": "Observe and analyze the current situation or environment.",
        "priority": 5,
    },
    "error": {
        "func": lambda *args, **kwargs: {"error": "An error occurred"},
        "description": "Handle error situations and provide appropriate responses.",
        "priority": 1,
    },
}
