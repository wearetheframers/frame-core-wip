import asyncio
import logging
import json
from typing import Dict, Any, Callable, Optional, TYPE_CHECKING, Union
from frame.src.framer.agency.actions import BaseAction

if TYPE_CHECKING:
    from frame.src.services import ExecutionContext

logger = logging.getLogger(__name__)
from frame.src.framer.agency.default_actions import (
    VALID_ACTIONS,
    extend_valid_actions,
)
from frame.src.framer.agency.actions import (
    CreateNewAgentAction,
    GenerateRolesAndGoalsAction,
    ObserveAction,
    RespondAction,
    ThinkAction,
    ResearchAction,
)


class ActionRegistry:
    def __init__(self, execution_context=None):
        self.actions: Dict[str, Dict[str, Any]] = {}
        self.execution_context = execution_context
        self.valid_actions = []
        self._register_default_actions()

    def set_framer(self, framer):
        self.framer = framer

    def _register_default_actions(self):
        default_actions = [
            CreateNewAgentAction(),
            GenerateRolesAndGoalsAction(),
            ObserveAction(),
            RespondAction(),
            ThinkAction(),
            ResearchAction(),
        ]
        for action in default_actions:
            self.add_action(
                action.name,
                description=action.description,
                action_func=getattr(action, 'func', None),
                priority=action.priority,
            )

    def extend_actions(self, new_actions: Dict[str, Dict[str, Any]]):
        extend_valid_actions(new_actions)
        self._register_default_actions()

    def add_action(
        self, name: str, description: str = "", action_func: Optional[Callable] = None, priority: int = 5
    ):
        """
        Add a new action to the registry.

        Args:
            name (str): The name of the action.
            action_func (Callable, optional): The function to execute for this action. Defaults to None.
            description (str, optional): A description of the action. Defaults to "".
            priority (int, optional): The priority of the action. Defaults to 5.
        """
        if priority is not None and not (1 <= priority <= 10):
            raise ValueError("Priority must be between 1 and 10")
        if action_func is None:
            # set action func to a dummy function
            action_func = lambda *args, **kwargs: None
        self.actions[name] = {
            "action_func": action_func,
            "description": description,
            "priority": priority,
        }
        if name not in self.valid_actions:
            self.valid_actions.append(name)

    def remove_action(self, name: str):
        """
        Remove an action from the registry.

        Args:
            name (str): The name of the action to remove.
        """
        if name in self.actions:
            del self.actions[name]
            if name in self.valid_actions:
                del self.valid_actions[name]
        else:
            raise ValueError(f"Action '{name}' not found.")
        return self.actions.get(name, {})

    def get_action(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve an action from the registry.

        Args:
            name (str): The name of the action to retrieve.

        Returns:
            Optional[Dict[str, Any]]: The action details if found, otherwise None.
        """
        return self.actions.get(name)

    def get_all_actions(self) -> Dict[str, Dict[str, Any]]:
        """
        Return all actions in the registry that are also in self.valid_actions.
        """
        return {k: v for k, v in self.actions.items() if k in self.valid_actions}

    async def perform_action(
        self,
        name: str,
        *args,
        callback: Optional[Callable] = None,
        callback_args: Optional[tuple] = (),
        **kwargs,
    ):
        action = self.get_action(name)
        if not action:
            raise ValueError(f"Action '{name}' not found")
        if self.execution_context is None:
            raise ValueError("Execution context is not set")
        response = await action["action_func"](*args, **kwargs)
        role = response if isinstance(response, dict) else response
        if callback:
            callback(response, *callback_args)
        return response

    def get_action(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve an action from the registry.

        Args:
            name (str): The name of the action to retrieve.

        Returns:
            Optional[Dict[str, Any]]: The action details if found, otherwise None.
        """
        return self.actions.get(name)

    async def execute_action(self, action_name: str, parameters: dict):
        """Execute an action by its name."""
        action = self.get_action(action_name)
        if action:
            # Filter parameters to match the expected arguments of the action function
            action_func = action["action_func"]
            expected_params = action_func.__code__.co_varnames[:action_func.__code__.co_argcount]
            filtered_params = {k: v for k, v in parameters.items() if k in expected_params}
            # Ensure 'query' is included in the parameters
            if 'query' not in filtered_params and 'text' in parameters:
                filtered_params['query'] = parameters['text']
            return await action_func(self.execution_context, **filtered_params)
        else:
            raise ValueError(f"Action '{action_name}' not found in the registry.")
