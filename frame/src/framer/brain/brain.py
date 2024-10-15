import json
import logging
import ast
import time
import asyncio
from typing import Any, Dict, List, Optional, TYPE_CHECKING
from frame.src.framer.agency import Agency
from frame.src.framer.brain.perception import Perception
from frame.src.framer.agency import ActionRegistry
from frame.src.framer.brain.decision import Decision
from frame.src.framer.brain.mind import Mind
from frame.src.framer.brain.memory import Memory
from frame.src.utils.llm_utils import get_llm_provider, get_completion
from frame.src.services.llm.main import LLMService
from asyncio import Future
from frame.src.services.llm.llm_adapters.lmql.lmql_adapter import LMQLConfig

logger = logging.getLogger(__name__)


class Brain:
    """
    The Brain class represents the decision-making component of the Framer.

    It processes perceptions, makes decisions, and executes actions based on those decisions.
    The Brain uses a set of VALID_ACTIONS to determine which actions can be executed.
    VALID_ACTIONS are derived from the ActionRegistry and default actions.
    """

    # Initialize VALID_ACTIONS from ActionRegistry and default actions
    VALID_ACTIONS = ActionRegistry().actions

    def __init__(
        self,
        llm_service: LLMService,
        roles: List[Dict[str, Any]],
        goals: List[Dict[str, Any]],
        default_model: str = "gpt-3.5-turbo",
        use_local_model: bool = False,
        valid_actions: Optional[List[str]] = None,
    ):
        """
        Initialize the Brain with the necessary components.

        Args:
            llm_service (LLMService): The language model service to use.
            roles (List[Dict[str, Any]]): Initial roles for the Brain.
            goals (List[Dict[str, Any]]): Initial goals for the Brain.
            default_model (str): The default language model to use.
            use_local_model (bool): Whether to use a local language model.
            valid_actions (Optional[List[str]]): A list of valid actions that the Brain can execute.
        """
        self.llm_service = llm_service
        self.default_model = default_model
        self.roles = roles
        self.goals = goals
        self.use_local_model = use_local_model

        self.mind = Mind(self)

        memory_config = {
            "llm": {
                "provider": get_llm_provider(self.use_local_model, self.default_model),
                "config": {
                    "model": self.default_model,
                },
            }
        }
        self.memory = Memory(memory_config)
        
        # Initialize ActionRegistry and VALID_ACTIONS
        self.action_registry = ActionRegistry()
        self.valid_actions = valid_actions or self.VALID_ACTIONS

        self.agency = Agency(llm_service=llm_service, context=None)

    def parse_json_response(self, response: str) -> Any:
        """
        Parse JSON response and handle potential errors.

        Args:
            response (str): The JSON response string to parse.

        Returns:
            Any: The parsed JSON data or an error dictionary.
        """
        try:
            return json.loads(response)
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error: {e}")
            logger.error(f"Raw response: {response}")

            # Check if the response is wrapped in a code block and remove it if present
            if response.startswith("```") and response.endswith("```"):
                cleaned_response = "\n".join(response.split("\n")[1:-1])
                try:
                    return json.loads(cleaned_response)
                except json.JSONDecodeError:
                    pass  # If this also fails, continue to the error return

            return {
                "action": "error",
                "parameters": {
                    "error": "Invalid JSON response",
                    "raw_response": response,
                },
                "reasoning": "Failed to parse the decision data.",
                "confidence": 0.0,
                "priority": 1,
            }

    def set_roles(self, roles: List[Dict[str, Any]]) -> None:
        """
        Set the roles for the Agency.

        Args:
            roles (List[Dict[str, Any]]): List of role dictionaries to set.
        """
        self.roles = roles
        self.agency.set_roles(roles)

    async def process_perception(
        self, perception: Perception, goals: Optional[List[Dict[str, Any]]] = None
    ) -> Decision:
        """
        Process a perception and make a decision based on it.

        Args:
            perception (Perception): The perception to process.
            goals (Optional[List[Dict[str, Any]]]): List of goal dictionaries to set.

        Returns:
            Decision: The decision made based on the perception.
        """
        if goals is not None:
            self.goals = goals
            self.agency.set_goals(goals)

        self.mind.perceptions.append(perception)
        decision = await self.make_decision(perception)
        if hasattr(self, "framer") and getattr(self.framer, "can_execute", False):
            await self.execute_decision(decision)
        return decision

    async def make_decision(self, perception: Optional[Perception] = None) -> Decision:
        """
        Make a decision on what action to take next based on the current state and perception.

        Args:
            perception (Optional[Perception]): The current perception of the environment.

        Returns:
            Decision: The decision made based on the current state and perception,
                      including the action to take, parameters, reasoning, confidence,
                      and priority (1-10 scale).
        """
        if perception is None:
            return Decision(action="no_action", reasoning="No perception provided")

        response = await self._get_decision_prompt(perception)
        decision_data = self.parse_json_response(response)

        logger.debug(f"Decision data received: {decision_data}")

        if decision_data.get("action") == "error":
            logger.error(
                f"Error in decision making: {decision_data.get('parameters', {}).get('error')}"
            )
            return Decision(**decision_data)

        action = decision_data.get("action", "no_action").lower()
        valid_actions = [action.lower() for action in self.action_registry.actions.keys()]
        
        if action not in valid_actions:
            logger.warning(
                f"Invalid action '{action}' generated. "
                f"Valid actions are: {', '.join(valid_actions)}"
            )
            logger.info(f"Attempting to execute action '{action}' anyway.")
        else:
            logger.info(f"Valid action '{action}' generated: {decision_data}")

        parameters = decision_data.get("parameters", {})
        if "topic" in parameters:
            parameters["research_topic"] = parameters.pop("topic")
        if not isinstance(parameters, dict):
            parameters = {"value": parameters}

        reasoning = decision_data.get("reasoning", "No reasoning provided.")

        return Decision(
            action=action,
            parameters=parameters,
            reasoning=reasoning,
            confidence=float(decision_data.get("confidence", 0.5)),
            priority=int(decision_data.get("priority", 5)),
        )

    async def execute_decision(self, decision: Decision):
        """
        Execute the decision made by the brain.

        Args:
            decision (Decision): The decision to execute.
        """
        logger.debug(f"Executing decision: {decision.action}")
        logger.debug(f"Decision parameters: {decision.parameters}")

        try:
            action_info = self.action_registry.get_action(decision.action)
            if action_info:
                action_func = action_info.get("action_func")
                if action_func:
                    if asyncio.iscoroutinefunction(action_func):
                        result = await action_func(self, **decision.parameters)
                    else:
                        result = action_func(self, **decision.parameters)
                    logger.info(f"Executed action: {decision.action}")
                    logger.debug(f"Action result: {result}")
                else:
                    logger.warning(f"No function found for action: {decision.action}")
            else:
                logger.warning(f"Unknown action: {decision.action}")

            logger.info(f"Executed decision: {decision.action}")
            logger.debug(f"Decision reasoning: {decision.reasoning}")

        except Exception as e:
            logger.error(f"Error executing decision: {e}")
            logger.exception("Detailed traceback:")

        if decision.action == "think":
            await self._generate_new_query(decision)

    async def _generate_new_query(self, decision: Decision) -> str:
        """
        Generate a new query based on the decision.

        Args:
            decision (Decision): The decision to base the new query on.

        Returns:
            str: The generated query.
        """
        prompt = (
            f"Based on the following decision, generate a new query or thought:\n\n"
            f"Decision: {decision.to_dict()}\n\nNew query:"
        )
        response = await self.llm_service.get_completion(
            prompt, model=self.default_model
        )
        return response.strip()

    async def _get_decision_prompt(self, perception: Optional[Perception]) -> str:
        """
        Generate a decision prompt based on the current perception and context.

        Args:
            perception (Optional[Perception]): The current perception.

        Returns:
            str: The generated decision prompt.
        """
        valid_actions = [
            action.lower() for action in self.action_registry.actions.keys()
        ]
        action_descriptions = "\n".join(
            [
                f"- {name.lower()}: {info['description']}"
                for name, info in self.action_registry.actions.items()
            ]
        )

        valid_actions_list = list(self.action_registry.actions.keys())
        prompt = f"""Given the following perception, decide on the most appropriate action to take.
        Perception: {perception}
        Current roles: {self.roles}
        Current goals: {self.goals}

        Consider the following possible actions:
        {action_descriptions}

        Valid actions are:
        {json.dumps({action.lower(): self.action_registry.actions[action]['description'] for action in self.action_registry.actions}, indent=2)}

        For each perception, carefully evaluate:
        - The type and content of the perception
        - The urgency and importance of the information
        - The current goals and roles of the system
        - Whether immediate action, further research, or no action is most appropriate

        Respond with a JSON object containing the following fields:
        - action: The action to take (must be EXACTLY one of the valid action names listed above)
        - parameters: Any relevant parameters for the action (e.g., new roles, goals, tasks, research topic, or response content)
        - reasoning: Your reasoning for this decision
        - confidence: A float between 0 and 1 indicating your confidence in this decision
        - priority: A number between 1-10 indicating the priority of this decision

        Ensure your decision is well-reasoned, aligns with the current goals and roles, and uses only the valid actions provided.
        """

        response = await self.llm_service.get_completion(
            prompt,
            model=self.default_model,
            additional_context={"valid_actions": valid_actions},
            expected_output=f"""
            {{
                "action": str where str in {valid_actions_list},
                "parameters": dict,
                "reasoning": str,
                "confidence": float where 0 <= float <= 1,
                "priority": int where 1 <= int <= 10
            }}
            """,
        )
        logger.debug(f"Raw LLM response: {response}")

        if response is None:
            logger.error("Received None response from LLM service.")
            return json.dumps(
                {
                    "action": "think",
                    "parameters": {
                        "thought": "Error: Received no response from language model."
                    },
                    "reasoning": "Failed to generate a valid decision due to no response",
                    "confidence": 0.0,
                    "priority": 1,
                }
            )

        # Check if ```json is in the response and remove it if present
        if (
            isinstance(response, str)
            and response.startswith("```json")
            and response.endswith("```")
        ):
            cleaned_response = "\n".join(response.split("\n")[1:-1])
            try:
                return cleaned_response
            except json.JSONDecodeError:
                pass

        # Parse the response
        try:
            decision_data = (
                json.loads(response) if isinstance(response, str) else response
            )

            # Ensure 'respond' is used instead of 'generate_response'
            if decision_data.get("action") == "generate_response":
                decision_data["action"] = "respond"
            if (
                "parameters" in decision_data
                and "response_content" in decision_data["parameters"]
            ):
                decision_data["parameters"]["content"] = decision_data[
                    "parameters"
                ].pop("response_content")

            # Double-check that the action is valid
            if decision_data["action"] not in self.action_registry.actions:
                logger.warning(
                    f"Invalid action: {decision_data['action']}. Defaulting to 'think'."
                )
                decision_data["action"] = "think"
                decision_data["reasoning"] = (
                    f"Invalid action '{decision_data['action']}' was generated. "
                    f"Defaulted to 'think'."
                )

            # Ensure the decision_data is properly formatted
            decision_data = {
                "action": decision_data.get("action", "respond"),
                "parameters": decision_data.get("parameters", {}),
                "reasoning": decision_data.get("reasoning", "No reasoning provided."),
                "confidence": float(decision_data.get("confidence", 0.5)),
                "priority": int(decision_data.get("priority", 5)),
            }

            return json.dumps(decision_data)
        except Exception as e:
            logger.error(f"Error parsing decision: {e}")
            logger.error(f"Raw response that caused the error: {response}")
            return json.dumps(
                {
                    "action": "think",
                    "parameters": {
                        "thought": f"Error: {str(e)}. Unable to process the request."
                    },
                    "reasoning": "Failed to generate a valid decision",
                    "confidence": 0.0,
                    "priority": 1,
                }
            )
