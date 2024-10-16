import asyncio
import logging
import json
from typing import Dict, Any, Callable, Optional
from frame.src.framer.agency.actions.observe import observe
from frame.src.framer.agency.actions.think import think
from frame.src.framer.agency.actions.respond import respond

logger = logging.getLogger(__name__)
from frame.src.framer.agency.default_actions import (
    VALID_ACTIONS,
    extend_valid_actions,
)
from frame.src.framer.agency.execution_context import ExecutionContext


class ActionRegistry:
    def __init__(self, execution_context: ExecutionContext):
        self.actions: Dict[str, Dict[str, Any]] = {}
        self.execution_context = execution_context
        self._register_default_actions()

    def set_execution_context(self, execution_context: ExecutionContext):
        self.execution_context = execution_context

    def _register_default_actions(self):
        for action, info in VALID_ACTIONS.items():
            self.register_action(
                action,
                info["func"],
                description=info["description"],
                priority=info["priority"],
            )

    def extend_actions(self, new_actions: Dict[str, Dict[str, Any]]):
        extend_valid_actions(new_actions)
        self._register_default_actions()

    def register_action(
        self, name: str, action_func: Callable, description: str = "", priority: int = 5
    ):
        if not (1 <= priority <= 10):
            raise ValueError("Priority must be between 1 and 10")
        if not asyncio.iscoroutinefunction(action_func):

            async def wrapper(*args, **kwargs):
                return action_func(*args, **kwargs)

            action_func = wrapper
        self.actions[name] = {
            "action_func": action_func,
            "description": description,
            "priority": priority,
        }

    def add_action(
        self, name: str, action_func: Callable, description: str = "", priority: int = 5
    ):
        """
        Add a new action to the registry.

        Args:
            name (str): The name of the action.
            action_func (Callable): The function to execute for this action.
            description (str, optional): A description of the action. Defaults to "".
            priority (int, optional): The priority of the action. Defaults to 5.
        """
        if not (1 <= priority <= 10):
            raise ValueError("Priority must be between 1 and 10")
        self.actions[name] = {
            "action_func": action_func,
            "description": description,
            "priority": priority,
        }
        VALID_ACTIONS[name] = {
            "func": action_func,
            "description": description,
            "priority": priority,
        }

    def remove_action(self, name: str):
        """
        Remove an action from the registry.

        Args:
            name (str): The name of the action to remove.
        """
        if name in self.actions:
            del self.actions[name]
            if name in VALID_ACTIONS:
                del VALID_ACTIONS[name]
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
        return self.actions

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
        response = await action["action_func"](
            *args, execution_context=self.execution_context, **kwargs
        )
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
            return await action["action_func"](self.execution_context, **parameters)
        else:
            raise ValueError(f"Action '{action_name}' not found in the registry.")
