import asyncio
import logging
import json
from typing import Dict, Any, Callable, Optional, TYPE_CHECKING, Union, List
from frame.src.framer.brain.actions import BaseAction
from frame.src.framer.brain.actions.error import ErrorAction

if TYPE_CHECKING:
    from frame.src.services import ExecutionContext
    from frame.src.framer.agency import GoleStatus, RoleStatus


from frame.src.framer.brain.default_actions import (
    DEFAULT_ACTIONS,
    extend_default_actions,
)
from frame.src.framer.brain.default_actions import (
    CreateNewAgentAction,
    GenerateRolesAndGoalsAction,
    ObserveAction,
    RespondAction,
    ThinkAction,
    ResearchAction,
)

logger = logging.getLogger(__name__)


class ActionRegistry:
    def __init__(self, execution_context: Optional["ExecutionContext"] = None):
        self.valid_actions = []
        self.actions: Dict[str, Dict[str, Any]] = {}
        self.execution_context = execution_context
        if not self.execution_context or not hasattr(
            self.execution_context, "llm_service"
        ):
            raise ValueError("ExecutionContext must have an llm_service set.")

        # Ensure llm_service is set in the execution context
        if not self.execution_context.llm_service:
            raise ValueError("ExecutionContext must have an llm_service set.")
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
            ErrorAction(),
        ]
        for action in default_actions:
            self.add_action(
                action.name,
                description=action.description,
                action_func=action.execute,
                priority=action.priority,
            )

    async def error_action(self, execution_context, error_message: str) -> str:
        """
        Handle errors by apologizing and attempting to continue the conversation.

        Args:
            execution_context: The execution context of the Framer.
            error_message (str): The error message to include in the response.

        Returns:
            str: A response apologizing for the error and attempting to continue the conversation.
        """
        soul_state = (
            execution_context.soul.get_current_state()
            if execution_context and execution_context.soul
            else "No soul state available."
        )
        recent_thoughts = (
            execution_context.mind.get_all_thoughts()[-5:]
            if execution_context and execution_context.mind
            else []
        )
        active_roles = (
            [role.name for role in execution_context.roles if role.status == "ACTIVE"]
            if execution_context
            else []
        )
        active_goals = (
            [goal.name for goal in execution_context.goals if goal.status == "ACTIVE"]
            if execution_context
            else []
        )
        # Check for streaming response in execution_context
        if hasattr(execution_context, "_streaming_response"):
            streaming_response = execution_context._streaming_response
        else:
            streaming_response = "No streaming response available."

        response = (
            f"I'm sorry, an error occurred: {error_message}. "
            "Let's try to continue our conversation.\n\n"
            "### Current Framer State\n"
            f"- Soul State: {soul_state}\n"
            f"- Recent Thoughts: {recent_thoughts}\n"
            f"- Active Roles: {active_roles}\n"
            f"- Active Goals: {active_goals}\n"
        )
        return response.strip() if isinstance(response, str) else str(response)

    def extend_actions(self, new_actions: Dict[str, Dict[str, Any]]):
        extend_default_actions(new_actions)
        self._register_default_actions()

    def add_action(
        self,
        action_or_name: Union[BaseAction, str],
        action_func: Optional[Callable] = None,
        description: str = "",
        priority: int = 5,
        expected_parameters: Optional[List[str]] = None,
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
            description = description or action_or_name.description
            action_func = action_func or getattr(action_or_name, "execute", None)
            priority = priority or action_or_name.priority
        else:
            name = action_or_name
            if not callable(action_func):
                raise ValueError(f"Action function for '{name}' must be callable.")

        if priority is not None and not (1 <= priority <= 10):
            raise ValueError("Priority must be between 1 and 10")
        if action_func is None:
            # Set action func to a default error handler
            async def action_func(execution_context, **kwargs):
                error_message = kwargs.get("error", "An error occurred.")
                return {"response": f"Error: {error_message}"}

        self.actions[name] = {
            "action_func": action_func,
            "description": description,
            "priority": priority,
            "expected_parameters": expected_parameters or [],
        }
        if not callable(action_func):
            raise ValueError(f"Action function for '{name}' must be callable.")
        if name not in self.valid_actions:
            self.valid_actions.append(name)
            logger.debug(f"Action '{name}' added to registry.")

    async def remove_action(self, name: str, plugin=None):
        """
        Remove an action from the registry.

        Args:
            name (str): The name of the action to remove.
        """
        try:
            if name in self.actions:
                action = self.actions.pop(name, None)
                if plugin and hasattr(plugin, "on_remove"):
                    await plugin.on_remove()
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
        # Validate action parameters before execution
        if not self._validate_parameters(name, kwargs):
            logger.error(f"Invalid parameters for action '{name}'. Aborting execution.")
            return

        action = self.get_action(name)
        if not action:
            raise ValueError(f"Action '{name}' not found")
        if self.execution_context is None:
            raise ValueError("Execution context is not set")
        if name == "get_weather":
            response = await action["action_func"](
                self.execution_context, city=kwargs.get("city")
            )
        else:
            response = await action["action_func"](
                self.execution_context, *args, **kwargs
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

    async def execute_action(self, action_name: str, **kwargs):
        """Execute an action by its name."""
        logger.debug(
            f"Available actions before executing '{action_name}': {list(self.actions.keys())}"
        )
        logger.info(f"Action name: {action_name}")

        if action_name == "no_action":
            logger.info("No action to execute. Skipping.")
            return None

        action = self.get_action(action_name)
        if not action:
            error_message = f"Action '{action_name}' not found in the registry."
            logger.error(error_message)
            return await self._handle_error(error_message)

        action_func = action["action_func"]
        result = {}
        try:
            # Don't pass execution_context if it's already in kwargs
            if "execution_context" in kwargs:
                _result = await action_func(**kwargs)
            else:
                _result = await action_func(self.execution_context, **kwargs)
            if _result is None:
                return {
                    "error": "Action returned None",
                    "fallback_response": "The action didn't produce a response. Please try again.",
                }
            elif isinstance(_result, dict):
                result = _result if "response" in _result else {"response": _result}
            elif isinstance(_result, (str, list)):
                result = {"response": _result}
            else:
                result = {"response": str(_result)}
            # Get reasoning or default empty string
            if _result is None:
                return {
                    "error": "Action returned None",
                    "fallback_response": "The action didn't produce a response. Please try again.",
                }
            if isinstance(_result, dict):
                result = _result
            else:
                result = {"response": _result}
        except Exception as e:
            error_message = f"Error executing action '{action_name}': {str(e)}"
            logger.error(error_message)
            return await self._handle_error(error_message)
        return result

    def set_execution_context(self, execution_context):
        self.execution_context = execution_context

    async def _handle_error(self, error_message: str):
        error_action = self.get_action("error")
        if error_action:
            return await error_action["action_func"](
                self.execution_context, error=error_message
            )
        else:
            return {
                "error": error_message,
                "fallback_response": "An error occurred while processing your request. Please try again.",
            }
