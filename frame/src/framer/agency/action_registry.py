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
            if action.name not in self.actions:
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
        self, action_or_name: Union[BaseAction, str], description: str = "", action_func: Optional[Callable] = None, priority: int = 5
    ):
        """
        Add a new action to the registry.

        Args:
            action_or_name (Union[BaseAction, str]): The action object or the name of the action.
            action_func (Callable, optional): The function to execute for this action. Defaults to None.
            description (str, optional): A description of the action. Defaults to "".
            priority (int, optional): The priority of the action. Defaults to 5.
        """
        if isinstance(action_or_name, BaseAction):
            name = action_or_name.name
            description = action_or_name.description
            action_func = getattr(action_or_name, 'execute', None)
            priority = action_or_name.priority
        else:
            name = action_or_name

        if priority is not None and not (1 <= priority <= 10):
            raise ValueError("Priority must be between 1 and 10")
        if action_func is None:
            # set action func to a dummy async function
            async def action_func(*args, **kwargs):
                return None
        self.actions[name] = {
            "action_func": action_func,
            "description": description,
            "priority": priority,
        }
        if name not in self.valid_actions:
            self.valid_actions.append(name)
            logger.debug(f"Action '{name}' added to registry.")

    def remove_action(self, name: str):
        """
        Remove an action from the registry.

        Args:
            name (str): The name of the action to remove.
        """
        try:
            if name in self.actions:
                del self.actions[name]
                if name in self.valid_actions:
                    self.valid_actions.remove(name)
            else:
                raise ValueError(f"Action '{name}' not found.")
        except Exception as e:
            logger.error(f"Error removing action '{name}': {e}")
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
        logger.info(f"Available actions before executing '{action_name}': {list(self.actions.keys())}")
        print("Action name: ", action_name)
        if action_name == "no_action":
            logger.info("No action to execute. Skipping.")
            return None

        action = self.get_action(action_name)
        if action:
            action_func = action["action_func"]
            expected_params = action_func.__code__.co_varnames[:action_func.__code__.co_argcount]
            filtered_params = {k: v for k, v in parameters.items() if k in expected_params}
            if 'query' in filtered_params and 'query' in parameters:
                del filtered_params['query']
            print("Filtered params: ", filtered_params)
            print("Expected params: ", expected_params)
            return await action_func(self.execution_context, **filtered_params)
        else:
            logger.error(f"Action '{action_name}' not found in the registry.")
            # raise ValueError(f"Action '{action_name}' not found in the registry.")
            return None
