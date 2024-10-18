import json
import logging
import ast
import time
import asyncio
from asyncio import Future
import re
from typing import Any, Dict, List, Optional, TYPE_CHECKING, Union
from frame.src.framer.agency import Agency
from frame.src.framer.brain.perception import Perception
from frame.src.framer.agency import ActionRegistry
from frame.src.framer.brain.decision import Decision
from frame.src.framer.brain.mind import Mind
from frame.src.framer.brain.memory import Memory
from frame.src.utils.llm_utils import get_llm_provider, get_completion
from frame.src.services.llm.main import LLMService
from frame.src.services.llm.llm_adapters.lmql.lmql_adapter import LMQLConfig
from frame.src.framer.soul.soul import Soul
from frame.src.framer.agency.roles import Role, RoleStatus
from frame.src.framer.agency.goals import Goal, GoalStatus
from frame.src.framer.agency.priority import Priority
from frame.src.services.execution_context import ExecutionContext
from frame.src.framer.config import FramerConfig

logger = logging.getLogger(__name__)


class Brain:
    """
    The Brain class represents the decision-making component of the Framer.

    It processes perceptions, makes decisions, and executes actions based on those decisions.
    The Brain uses a set of VALID_ACTIONS to determine which actions can be executed.
    VALID_ACTIONS are derived from the ActionRegistry and default actions.
    """

    def __init__(
        self,
        llm_service: LLMService,
        roles: List[Dict[str, Any]],
        goals: List[Dict[str, Any]],
        default_model: str = "gpt-3.5-turbo",
        recent_memories_limit: int = 5,
        soul: Optional[Soul] = None,
        execution_context: Optional[ExecutionContext] = None,
    ):
        """
        Initialize the Brain with the necessary components.

        Args:
            llm_service (LLMService): The language model service.
            roles (List[Dict[str, Any]]): Initial roles for the Brain.
            goals (List[Dict[str, Any]]): Initial goals for the Brain.
            default_model (str): The default language model to use.
            recent_memories_limit (int): The number of recent memories to keep. Defaults to 5.
            soul (Optional[Soul]): The Soul instance for the Brain.
            execution_context (Optional[ExecutionContext]): The execution context for the Brain.
        """
        self.llm_service = llm_service
        self.default_model = default_model
        self.roles = roles
        self.goals = goals
        self.soul = soul
        self.execution_context = execution_context or ExecutionContext(
            llm_service=llm_service,
            soul=soul,
            config=FramerConfig(name="DefaultFramer", default_model=default_model),
        )

        self.mind = Mind(self, recent_memories_limit)

        memory_config = {
            "llm": {
                "provider": get_llm_provider(self.default_model),
                "config": {
                    "model": self.default_model,
                },
            }
        }
        self.memory = Memory(memory_config)

        # Initialize ActionRegistry
        self.action_registry = ActionRegistry()

        # Initialize Agency
        self.agency = Agency(
            llm_service=self.llm_service,
            context=None,
            execution_context=ExecutionContext(
                llm_service=self.llm_service,
                process_perception=self.process_perception,
                execute_decision=self.execute_decision,
                config=FramerConfig(
                    name=(
                        self.framer.config.name
                        if hasattr(self, "framer")
                        else "DefaultFramer"
                    ),
                    default_model=self.default_model,
                ),
            ),
        )

        # Register the respond action using the agency's perform_task method
        self.action_registry.register_action(
            "respond",
            self.agency.perform_task,
            description="Generate a response based on the current context",
            priority=5,
        )

        # Update the agency's action_registry
        self.agency.action_registry = self.action_registry

    def set_framer(self, framer):
        self.framer = framer
        if hasattr(self.agency, "set_framer"):
            self.agency.set_framer(framer)
        else:
            logger.warning(
                "Agency does not have a set_framer method. This might cause issues."
            )

    def get_framer(self):
        return self.framer

    async def _execute_think_action(self, decision: Decision) -> Dict[str, Any]:
        """
        Execute the 'think' action, which involves pondering on various aspects and potentially creating new tasks.

        Args:
            decision (Decision): The decision to execute.

        Returns:
            Dict[str, Any]: A dictionary containing the result of the think action, including:
                - analysis (str): Analysis of the current situation.
                - new_tasks (List[Dict[str, Any]]): List of new tasks if any.
                - generate_new_prompt (bool): Whether a new prompt should be generated.
                - new_prompt (str): The new prompt if generate_new_prompt is True.
        """
        # Gather context for thinking
        soul_context = {}
        if (
            self.execution_context
            and hasattr(self.execution_context, "soul")
            and self.execution_context.soul
        ):
            soul_context = self.execution_context.soul.get_current_state()

        roles_and_goals = {"roles": self.roles, "goals": self.goals}
        recent_thoughts = self.mind.get_all_thoughts()[-5:]  # Get last 5 thoughts
        recent_perceptions = self.mind.get_recent_perceptions(5)
        execution_state = self.execution_context.state if self.execution_context else {}

    def parse_json_response(self, response: str) -> Any:
        """
        Parse JSON response and handle potential errors.

        Args:
            response (str): The JSON response string to parse.

        Returns:
            Any: The parsed JSON data or an error dictionary.
        """
        try:
            # Remove trailing commas from the response
            response = re.sub(r",\s*}", "}", response)
            response = re.sub(r",\s*]", "]", response)
            return json.loads(response)
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error: {e}")
            logger.error(f"Raw response: {response}")

            # Check if the response is wrapped in a code block and remove it if present
            if response.startswith("```") and response.endswith("```"):
                cleaned_response = "\n".join(response.split("\n")[1:-1])
                try:
                    # Remove trailing commas from the cleaned response
                    cleaned_response = re.sub(r",\s*}", "}", cleaned_response)
                    cleaned_response = re.sub(r",\s*]", "]", cleaned_response)
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

    def set_roles(self, roles: List[Role]) -> None:
        """
        Set the roles for the Agency.

        Args:
            roles (List[Role]): List of Role objects to set.
        """
        self.roles = roles
        self.agency.set_roles(roles)

    async def process_perception(
        self,
        perception: Union[Perception, Dict[str, Any]],
        goals: Optional[List[Goal]] = None,
    ) -> Decision:
        """
        Process a perception and make a decision based on it.

        Args:
            perception (Union[Perception, Dict[str, Any]]): The perception to process.
            goals (Optional[List[Goal]]): List of Goal objects to set.

        Returns:
            Decision: The decision made based on the perception.
        """
        if goals is not None:
            self.goals = goals
            self.agency.set_goals(goals)

        # Convert perception to Perception object if it is a dictionary
        if isinstance(perception, dict):
            perception = Perception.from_dict(perception)

        self.mind.perceptions.append(perception)
        decision = await self.make_decision(perception)
        if decision is None:
            logger.error("Failed to make a decision. Returning default decision.")
            decision = Decision(
                action="error",
                parameters={},
                reasoning="Failed to make a decision",
                confidence=0.0,
                priority=1,
                related_roles=[],
                related_goals=[],
            )
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
                      and priority.
        """
        if perception is None:
            return Decision(
                action="no_action",
                parameters={},
                reasoning="No perception provided",
                confidence=0.0,
                priority=1,
                related_roles=[],
                related_goals=[],
            )

        response = await self._get_decision_prompt(perception)
        decision_data = self.parse_json_response(response)

        logger.debug(f"Decision data received: {decision_data}")

        action = decision_data.get("action", "respond").lower()
        valid_actions = [
            action.lower() for action in self.action_registry.actions.keys()
        ]

        # Check if the action is valid
        if action not in valid_actions:
            # If the action is not valid, check if it's related to web search or summarization
            if any(keyword in action for keyword in ["search", "summarize", "extract"]):
                action = "search_extract_summarize"
                decision_data["action"] = action
                decision_data["reasoning"] = (
                    f"Action '{action}' was generated based on the perception. "
                    f"Using the search_extract_summarize plugin to process this request."
                )
            else:
                invalid_action = action
                action = "respond"
                logger.warning(
                    f"Invalid action '{invalid_action}' generated. "
                    f"Valid actions are: {', '.join(valid_actions)}"
                )
                decision_data["action"] = action
                decision_data["reasoning"] = (
                    f"Invalid action '{invalid_action}' was generated. Defaulted to '{action}'."
                )

        logger.info(f"Action '{action}' generated: {decision_data}")

        parameters = decision_data.get("parameters", {})
        if "topic" in parameters:
            parameters["research_topic"] = parameters.pop("topic")
        if not isinstance(parameters, dict):
            parameters = {"value": parameters}

        reasoning = decision_data.get("reasoning", "No reasoning provided.")

        # Check if goals are None and generate them if necessary
        if self.agency.goals is None:
            _, self.agency.goals = await self.agency.generate_roles_and_goals()

        # Consider role and goal priorities when setting decision priority
        active_roles = [role for role in self.roles if role.status == RoleStatus.ACTIVE]
        active_goals = [goal for goal in self.goals if goal.status == GoalStatus.ACTIVE]
        roles_priority = max(
            [role.priority for role in active_roles], default=Priority.MEDIUM
        )
        goals_priority = max(
            [goal.priority for goal in active_goals], default=Priority.MEDIUM
        )
        priority_value = decision_data.get("priority", "MEDIUM")
        priority_int = Decision.convert_priority(priority_value)

        decision = Decision(
            action=action,
            parameters=parameters,
            reasoning=reasoning,
            confidence=float(decision_data.get("confidence", 0.5)),
            priority=priority_int,
            related_roles=[
                role for role in active_roles if role.priority >= priority_int
            ],
            related_goals=[
                goal for goal in active_goals if goal.priority >= priority_int
            ],
        )

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

        active_roles = [
            f"{role.name} (Priority: {role.priority.name}, Status: {role.status.name})"
            for role in self.roles
            if role.status == RoleStatus.ACTIVE
        ]
        active_goals = [
            f"{goal.name} (Priority: {goal.priority.name}, Status: {goal.status.name})"
            for goal in self.goals
            if goal.status == GoalStatus.ACTIVE
        ]

        prompt = f"""Given the following perception and context, decide on the most appropriate action to take.
        Perception: {perception}
        
        Current active roles:
        {json.dumps(active_roles, indent=2)}
        
        Current active goals:
        {json.dumps(active_goals, indent=2)}

        Consider the following possible actions:
        {action_descriptions}

        Valid actions are:
        {json.dumps({action.lower(): self.action_registry.actions[action]['description'] for action in self.action_registry.actions}, indent=2)}

        For each perception, carefully evaluate:
        - The type and content of the perception
        - The urgency and importance of the information
        - The current active goals and roles of the system, considering their priorities and statuses
        - Whether immediate action, further research, or no action is most appropriate

        Priority levels:
        {json.dumps({p.name: p.value for p in Priority}, indent=2)}

        Respond with a JSON object containing the following fields:
        - action: The action to take (must be EXACTLY one of the valid action names listed above)
        - parameters: Any relevant parameters for the action (e.g., new roles, goals, tasks, research topic, or response content)
        - reasoning: Your reasoning for this decision, including how it aligns with current roles and goals
        - confidence: A float between 0 and 1 indicating your confidence in this decision
        - priority: A string representing the priority level (e.g., "LOW", "MEDIUM", "HIGH", "CRITICAL") or an integer between 1 and 10 based on the urgency and importance of the action
        - related_roles: A list of role names that are most relevant to this decision
        - related_goals: A list of goal names that are most relevant to this decision

        Ensure your decision is well-reasoned, aligns with the current active goals and roles (considering their priorities), and uses only the valid actions provided.
        Use the provided priority levels when assigning priority to your decision, taking into account the priorities of related roles and goals.
        """

        valid_actions = list(self.action_registry.actions.keys())
        response = await self.llm_service.get_completion(
            prompt,
            model=self.default_model,
            additional_context={"valid_actions": valid_actions},
            expected_output=f"""
            {{
                "action": str where str in {valid_actions},
                "parameters": dict,
                "reasoning": str,
                "confidence": float where 0 <= float <= 1,
                "priority": str,
                "related_roles": list,
                "related_goals": list
            }}
            """,
        )
        logger.debug(f"Raw LLM response: {response}")

        return response

    async def execute_decision(self, decision: Decision):
        """
        Execute the decision made by the brain.

        Args:
            decision (Decision): The decision to execute.
        """
        logger.debug(f"Executing decision: {decision.action}")
        logger.debug(f"Decision parameters: {decision.parameters}")

        try:
            if decision.action == "think":
                result = await self._execute_think_action(decision)
            else:
                if decision.action not in self.action_registry.actions:
                    raise ValueError(
                        f"Action '{decision.action}' not found in registry."
                    )

                # For 'respond' action, ensure 'content' is passed correctly
                if decision.action == "respond":
                    # For 'respond' action, we'll use the agency's perform_task method directly
                    result = await self.agency.perform_task(
                        {
                            "description": decision.parameters.get("content", ""),
                            "workflow_id": "default",
                        }
                    )
                else:
                    result = await self.action_registry.execute_action(
                        decision.action, decision.parameters
                    )

            logger.info(f"Executed action: {decision.action}")
            logger.debug(f"Action result: {result}")

            logger.info(f"Executed decision: {decision.action}")
            logger.debug(f"Decision reasoning: {decision.reasoning}")

        except Exception as e:
            logger.error(f"Error executing decision: {e}")
            logger.exception("Detailed traceback:")
            result = {"error": str(e)}

        return result

    async def _execute_think_action(self, decision: Decision):
        """
        Execute the 'think' action, which involves pondering on various aspects and potentially creating new tasks.

        Args:
            decision (Decision): The decision to execute.

        Returns:
            Any: The result of the think action.
        """
        # Gather context for thinking
        soul_context = (
            self.execution_context.soul.get_current_state()
            if self.execution_context.soul
            else {}
        )
        roles_and_goals = {"roles": self.roles, "goals": self.goals}
        recent_thoughts = self.mind.get_all_thoughts()[-5:]  # Get last 5 thoughts
        recent_perceptions = self.mind.get_recent_perceptions(
            5
        )  # Use a fixed number instead of recent_perceptions_limit

        # Prepare the prompt for the LLM
        prompt = f"""
        Based on the following context, ponder and reflect on the current situation:

        Soul state: {soul_context}
        Roles and goals: {roles_and_goals}
        Recent thoughts: {recent_thoughts}
        Recent perceptions: {recent_perceptions}
        Execution state: {self.execution_context.state}

        Current decision: {decision.to_dict()}

        1. Analyze the current situation and provide insights.
        2. Determine if any new tasks or actions are necessary.
        3. If new tasks are needed, describe them in detail.
        4. Decide if a new prompt should be generated for better results.

        Respond with a JSON object containing:
        - analysis: Your analysis of the situation
        - new_tasks: A list of new tasks if any (each task should have 'description' and 'priority')
        - generate_new_prompt: Boolean indicating if a new prompt should be generated
        - new_prompt: The new prompt if generate_new_prompt is true
        """

        response = await self.llm_service.get_completion(
            prompt, model=self.default_model
        )
        result = json.loads(response)

        # Process the result
        self.mind.think(result["analysis"])

        if result["new_tasks"]:
            for task_data in result["new_tasks"]:
                new_task = self.agency.create_task(**task_data)
                self.agency.add_task(new_task)

        if result["generate_new_prompt"]:
            new_perception = Perception(
                type="thought", data={"query": result["new_prompt"]}
            )
            await self.process_perception(new_perception)

        return result

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

        Priority levels:
        {json.dumps({p.name: p.value for p in Priority}, indent=2)}

        Respond with a JSON object containing the following fields:
        - action: The action to take (must be EXACTLY one of the valid action names listed above)
        - parameters: Any relevant parameters for the action (e.g., new roles, goals, tasks, research topic, or response content)
        - reasoning: Your reasoning for this decision
        - confidence: A float between 0 and 1 indicating your confidence in this decision
        - priority: A string representing the priority level (e.g., "MEDIUM", "HIGH", etc.)

        Ensure your decision is well-reasoned, aligns with the current goals and roles, and uses only the valid actions provided.
        Use the provided priority levels when assigning priority to your decision.
        """

        valid_actions = list(self.action_registry.actions.keys())
        response = await self.llm_service.get_completion(
            prompt,
            model=self.default_model,
            additional_context={"valid_actions": valid_actions},
            expected_output=f"""
            {{
                "action": str where str in {valid_actions},
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
                    f"Invalid action: {decision_data['action']}. Defaulting to 'error'."
                )
                decision_data["action"] = "error"
                decision_data["reasoning"] = (
                    f"Invalid action '{decision_data['action']}' was generated. "
                    f"Defaulted to 'error'."
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
