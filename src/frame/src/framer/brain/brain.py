import json
import logging
import re
from typing import Any, Dict, List, Optional, Union, Callable, TYPE_CHECKING

logger = logging.getLogger(__name__)

from frame.src.utils.llm_utils import get_llm_provider
from frame.src.services import ExecutionContext, LLMService
from frame.src.models.framer.brain.decision.decision import Decision
from frame.src.framer.brain.decision.decision import DecisionStatus
from frame.src.framer.common.enums import ExecutionMode, DecisionStatus
from frame.src.framer.agency.roles import Role, RoleStatus
from frame.src.framer.agency.goals import Goal, GoalStatus
from frame.src.framer.agency.priority import Priority

from typing import TYPE_CHECKING
from frame.src.utils.decorators import log_execution, measure_performance

if TYPE_CHECKING:
    from frame.src.services import MemoryService
    from frame.src.framer.agency import Agency

from frame.src.framer.soul import Soul
from frame.src.framer.brain.memory import Memory
from frame.src.framer.brain.mind import Mind
from frame.src.framer.brain.mind.perception import Perception
from frame.src.framer.brain.action_registry import ActionRegistry
from frame.src.framer.config import FramerConfig

logger = logging.getLogger(__name__)


class Brain:
    """
    The Brain class represents the central decision-making and cognitive processing component of the Framer.

    Note: Plugins are lazily loaded. If a plugin does not have the necessary permissions, it will not be loaded until explicitly added with the required permissions.

    It is responsible for processing perceptions, making decisions, and executing actions based on those decisions.
    The Brain integrates various cognitive functions, including perception processing, decision-making,
    memory management, and action execution.

    Key features:
    - Perception processing: Analyzes and interprets incoming perceptions.
    - Decision-making: Generates decisions based on current context, roles, goals, and perceptions.
    - Action execution: Executes decided actions using the action registry.
    - Memory integration: Utilizes the memory service for storing and retrieving information.
    - LLM integration: Uses language models for generating responses and making decisions.
    - Role and goal management: Considers active roles and goals in the decision-making process.

    The Brain uses a set of valid actions, derived from the ActionRegistry and default actions,
    to determine which actions can be executed. This ensures that all actions are within the
    defined capabilities of the Framer.

    Attributes:
        llm_service (LLMService): The language model service for text generation and processing.
        default_model (str): The default language model to use.
        roles (List[Dict[str, Any]]): List of roles for the Brain.
        goals (List[Dict[str, Any]]): List of goals for the Brain.
        soul (Optional[Soul]): The Soul instance associated with this Brain.
        execution_context (Optional[ExecutionContext]): The execution context for the Brain.
        mind (Mind): The Mind instance for cognitive processing.
        memory_service (Optional[MemoryService]): The memory service for storing and retrieving information.
        action_registry (ActionRegistry): Registry of available actions.

    The Brain class serves as the cognitive core of the Framer, coordinating various components
    to enable intelligent decision-making and action execution.
    """

    def __init__(
        self,
        llm_service: LLMService,
        execution_context: Optional[ExecutionContext] = None,
        memory_service: Optional["MemoryService"] = None,
        roles: List[Dict[str, Any]] = [],
        goals: List[Dict[str, Any]] = [],
        default_model: str = "gpt-3.5-turbo",
        soul: Optional[Soul] = None,
    ):
        """
        Initialize the Brain with the necessary components.

        Args:
            llm_service (LLMService): The language model service.
            execution_context (Optional['ExecutionContext']): The execution context.
            memory_service (Optional[MemoryService]): The memory service.
            roles (List[Dict[str, Any]]): Initial roles for the Brain.
            goals (List[Dict[str, Any]]): Initial goals for the Brain.
            default_model (str): The default language model to use.
            soul (Optional[Soul]): The Soul instance for the Brain.
        """
        self.logger = logging.getLogger(__name__)
        self.llm_service = llm_service
        self.execution_context = execution_context or ExecutionContext(
            llm_service=self.llm_service, config=None
        )
        self.default_model = default_model
        self.roles = [
            Role(**role) if isinstance(role, dict) else role for role in roles
        ]
        self.goals = [
            Goal(**goal) if isinstance(goal, dict) else goal for goal in goals
        ]
        self.soul = soul
        self.memory_service = memory_service
        if self.memory_service:
            self.memory = Memory(self.memory_service)
        else:
            self.logger.warning("No memory service provided, Memory object not created")
            self.memory = None

        self.mind = Mind(self)
        self.action_registry = ActionRegistry(execution_context=self.execution_context)
        if not isinstance(self.execution_context, ExecutionContext):
            raise TypeError("execution_context must be an instance of ExecutionContext")

    def set_memory_service(self, memory_service: Optional["MemoryService"]):
        """
        Set the memory service for the Brain.

        Args:
            memory_service (Optional[MemoryService]): The memory service to set.
        """
        self.memory_service = memory_service
        if self.memory_service:
            self.memory = Memory(self.memory_service)
            logger.info(f"Set memory service: {self.memory_service}")
        else:
            self.memory = None
            logger.warning(
                "Memory service is not set. Memory operations will not be available."
            )

    async def set_framer(self, framer):
        self.framer = framer
        self.action_registry.set_execution_context(self.execution_context)
        for plugin in getattr(framer, "plugins", {}).values():
            if hasattr(plugin, "on_remove"):
                await plugin.on_remove()

    def get_framer(self):
        return self.framer

    async def _execute_think_action(self, decision: "Decision") -> Dict[str, Any]:
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
        # Prepare the prompt for the LLM
        prompt = f"""
        Based on the following context, ponder and reflect on the current situation:
        
        Soul state: {soul_context}
        Roles and goals: {roles_and_goals}
        Recent thoughts: {recent_thoughts}
        Recent perceptions: {recent_perceptions}

        Current decision: {decision.to_dict()}

        1. Analyze the current situation and provide insights.
        2. Determine if any new tasks or actions are necessary.
        3. If new tasks are needed, describe them in detail.
        4. Decide if a new prompt should be generated for better results.

        Respond with a JSON object containing the following fields:
        - analysis: Analysis of the current situation.
        - new_tasks: A list of new tasks if any (each task should have 'description' and 'priority').
        - generate_new_prompt: A boolean indicating whether a new prompt should be generated.
        - new_prompt: The new prompt to use if generate_new_prompt is True.
        """
        try:
            result = await self.llm_service.get_completion(
                prompt,
                model=self.default_model,
                expected_output=f"""
                {{
                    "analysis": str,
                    "new_tasks": list,
                    "generate_new_prompt": bool,
                    "new_prompt": str
                }}
                """,
            )
            return result
        except Exception as e:
            logger.error(f"Error in _execute_think_action: {str(e)}")
            return {"error": str(e)}

    def parse_json_response(self, response: Any) -> Any:
        """
        Parse JSON response and handle potential errors.

        Args:
            response (Any): The response to parse, which could be a string or a dictionary.

        Returns:
            Any: The parsed JSON data or an error dictionary.
        """
        if response is None:
            logger.error("Received None response, cannot parse JSON.")
            result = {
                "action": "error",
                "parameters": {
                    "error": "Received None response",
                    "raw_response": str(response),
                },
                "reasoning": "Failed to parse the decision data due to None response.",
                "confidence": 0.0,
                "priority": 1,
            }
            return result

        if isinstance(response, dict):
            # If response is already a dictionary, return it as is
            return response

        try:
            # If response is a string, try to parse it as JSON
            if isinstance(response, str):
                # Remove trailing commas from the response
                response = re.sub(r",\s*}", "}", response)
                response = re.sub(r",\s*]", "]", response)
                decision_data = json.loads(response)
            else:
                raise ValueError(f"Unexpected response type: {type(response)}")

            # Ensure priority is a Priority enum
            priority_value = decision_data.get("priority", Priority.MEDIUM)
            try:
                decision_data["priority"] = Priority.get(priority_value).value
            except (KeyError, ValueError) as e:
                logger.error(f"Invalid priority: {priority_value}. Error: {e}")
                decision_data["priority"] = Priority.MEDIUM.value
            return decision_data
        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"Parsing error: {e}")
            logger.error(f"Raw response: {response}")

            return {
                "action": "error",
                "parameters": {
                    "error": f"Invalid response: {str(e)}",
                    "raw_response": str(response),
                },
                "reasoning": "Failed to parse the decision data.",
                "confidence": 0.0,
                "priority": 1,
            }

    def set_roles(self, roles: List["Role"]) -> None:
        """
        Set the roles for the Agency.

        Args:
            roles (List[Role]): List of Role objects to set.
        """
        self.roles = roles
        self.execution_context.set_roles(roles)

    @log_execution
    @measure_performance
    async def process_perception(
        self,
        perception: Union["Perception", Dict[str, Any]],
        goals: Optional[List["Goal"]] = None,
    ) -> "Decision":
        """
        Process a perception and make a decision based on it.

        Args:
            perception (Union['Perception', Dict[str, Any]]): The perception to process.
            goals (Optional[List[Goal]]): List of Goal objects to set.

        Returns:
            Decision: The decision made based on the perception.
        """

        if goals is not None:
            self.goals = goals
            self.execution_context.set_goals(goals)

        # Convert perception to Perception object if it is a dictionary
        if isinstance(perception, dict):
            perception = Perception.from_dict(perception)
        elif not isinstance(perception, Perception):
            raise TypeError("Perception must be a Perception object or a dictionary.")
        else:
            perception = Perception.from_dict(perception.to_dict())

        self.mind.perceptions.append(perception)
        available_actions = self.action_registry.get_all_actions().keys()
        self.logger.debug(f"Processing perception: {perception}")
        self.logger.debug(f"Avaliable actions: {available_actions}")
        decision = await self.make_decision(perception)
        if hasattr(self, "framer") and getattr(self.framer, "can_execute", False):
            if decision is None:
                self.logger.warning("No decision was made for the given perception.")
                return None
            if not decision.reasoning:
                decision.reasoning = (
                    "Reasoning not provided. Encourage detailed reasoning."
                )
            # Check if the decision has already been executed
            if (
                not hasattr(self, "_last_executed_decision")
                or self._last_executed_decision != decision
            ):
                await self.execute_decision(decision, perception)
                self._last_executed_decision = decision
            else:
                self.logger.info(
                    "Decision has already been executed, skipping re-execution."
                )
        else:
            logger.warn("Framer is not ready to execute decisions. Queuing perception.")
            # Code to queue the perception can be added here if needed
        return decision

    async def make_decision(
        self, perception: Optional[Perception] = None
    ) -> "Decision":
        """
        Make a decision on what action to take next based on the current state and perception.

        Args:
            perception (Optional[Perception]): The current perception of the environment.

        Returns:
            Decision: The decision made based on the current state and perception,
                      including the action to take, parameters, reasoning, confidence,
                      and priority.
        """
        from frame.src.framer.brain.decision import Decision

        # If no perception is provided, return a default decision with no action
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

        # Get a decision prompt based on the current perception
        response = await self._get_decision_prompt(perception)

        if response is None or (isinstance(response, str) and not response.strip()):
            logger.error("Received empty or None response from LLM service")
            return Decision(
                action="error",
                parameters={"error": "Empty or None response from LLM service"},
                reasoning="Failed to get a valid response from the language model",
                confidence=0.0,
                priority=1,
                related_roles=[],
                related_goals=[],
            )

        # Parse the response from the LLM service to extract decision data
        decision_data = self.parse_json_response(response)

        logger.debug(f"Decision data received: {decision_data}")

        if isinstance(decision_data, dict) and "error" in decision_data:
            logger.error(f"Error in decision making: {decision_data['error']}")
            return Decision(
                action="error",
                parameters={"error": decision_data["error"]},
                reasoning="Error occurred during decision making",
                confidence=0.0,
                priority=1,
                related_roles=[],
                related_goals=[],
            )

        # Use default action 'respond' if no action is provided
        try:
            action = decision_data.get("action", "respond")
        except:
            action = "no_action"
        valid_actions = [
            str(action).lower()
            for action in self.action_registry.get_all_actions().keys()
        ]

        # Retrieve context from the execution context
        # If the context indicates high urgency and risk, choose an adaptive decision
        context = self.execution_context.get_full_state()
        # Determine the best action based on context
        if context.get("urgency", 0) > 7 and context.get("risk", 0) > 5:
            action = "adaptive_decision"
            decision_data["action"] = action
            decision_data["reasoning"] = (
                f"High urgency and risk detected. Using '{action}' to adaptively decide the best course of action."
            )

        logger.info(f"Decision made: {decision_data}")

        # Merge perception data into parameters
        parameters = decision_data.get("parameters", {})
        if not isinstance(parameters, dict):
            parameters = {}
        if perception and perception.data:
            # Ensure that perception data is considered
            parameters = {**perception.data, **parameters}

        reasoning = decision_data.get("reasoning", "No reasoning provided.")

        # Check if goals are None and generate them if necessary
        # This ensures that the decision-making process has relevant goals to consider
        if self.execution_context and not self.execution_context.get_goals():
            # Assuming the execution_context has a method to generate goals
            goals = await self.execution_context.generate_goals()
            self.execution_context.set_goals(goals)

        # Consider role and goal priorities when setting decision priority
        # This helps in aligning the decision with the most critical roles and goals
        active_roles = [role for role in self.roles if role.status == RoleStatus.ACTIVE]
        active_goals = [
            goal
            for goal in self.execution_context.get_goals()
            if goal.status == GoalStatus.ACTIVE
        ]
        roles_priority = max(
            [role.priority for role in active_roles], default=Priority.MEDIUM
        )
        goals_priority = max(
            [goal.priority for goal in active_goals], default=Priority.MEDIUM
        )
        
        # Ensure priority is a Priority enum
        priority_value = decision_data.get("priority", Priority.MEDIUM)
        try:
            if isinstance(priority_value, str):
                priority_enum = Priority[priority_value.upper()]
            elif isinstance(priority_value, int):
                priority_enum = Priority(priority_value)
            elif isinstance(priority_value, Priority):
                priority_enum = priority_value
            else:
                raise ValueError(f"Unexpected priority type: {type(priority_value)}")
        except (KeyError, ValueError) as e:
            logger.error(f"Invalid priority: {priority_value}. Error: {e}")
            priority_enum = Priority.MEDIUM

        priority_int = priority_enum.value

        # Convert related_roles and related_goals to Role and Goal instances
        related_roles = [
            role
            for role in active_roles
            if role.name in decision_data.get("related_roles", [])
        ]
        related_goals = [
            goal
            for goal in active_goals
            if goal.name in decision_data.get("related_goals", [])
        ]

        # Ensure parameters is a dictionary
        parameters = decision_data.get("parameters", {})
        if not isinstance(parameters, dict):
            parameters = {}

        # Ensure parameters includes the query and execution context for memory retrieval
        if decision_data.get("action") == "respond with memory retrieval":
            parameters = {} if isinstance(parameters, list) else parameters
            if perception and perception.data:
                parameters.update(
                    {
                        "query": perception.data.get("text", ""),
                        "execution_context": self.execution_context,
                        "llm_service": self.llm_service,
                    }
                )
                from frame.src.constants.user import DEFAULT_USER_ID

                parameters["user_id"] = parameters.get("user_id", DEFAULT_USER_ID)

        decision = Decision(
            action=decision_data.get("action", "respond"),
            parameters=parameters,
            reasoning=decision_data.get("reasoning", "No reasoning provided."),
            confidence=float(decision_data.get("confidence", 0.5)),
            priority=priority_int,
            related_roles=related_roles,
            related_goals=related_goals,
        )
        
        logger.info(f"Final decision object: {decision}")
        
        if hasattr(decision, "reasoning"):
            decision.reasoning += f" (Aligned with {len(active_goals)} active goals)"
        else:
            logger.error("Decision object does not have a 'reasoning' attribute.")
            
        decision.result = decision.parameters.get("response_content", None)
        return decision

    async def _get_decision_prompt(self, perception: Optional[Perception]) -> str:
        """
        Generate a decision prompt based on the current perception and context.

        Args:
            perception (Optional[Perception]): The current perception.

        Returns:
            str: The generated decision prompt.
        """
        valid_actions = self.action_registry.get_all_actions()
        logger.debug(f"Valid actions: {valid_actions}")

        active_roles = [
            f"{role.name} (Priority: {role.priority}, Status: {role.status.name})"
            for role in self.roles
            if role.status == RoleStatus.ACTIVE
        ]
        active_goals = [
            f"{goal.name} (Priority: {goal.priority}, Status: {goal.status.name})"
            for goal in self.goals
            if goal.status == GoalStatus.ACTIVE
        ]

        prompt = f"""Given the following perception and context, decide on the most appropriate action to take.
        Perception: {perception}
        Perception Data: {perception.data}
        
        Current active roles:
        {json.dumps(active_roles, indent=2)}
        
        Current active goals:
        {json.dumps(active_goals, indent=2)}

        Valid actions are:
        {json.dumps({action_name: {"description": action_info["description"], "expected_parameters": action_info.get("expected_parameters", []), "priority": action_info["priority"]} for action_name, action_info in self.action_registry.actions.items()}, indent=2)}
        
        For each perception, carefully evaluate:
        - The type and content of the perception
        - The urgency and importance of the information
        - The current active goals and roles of the system, considering their priorities and statuses
        - Whether immediate action, further research, or no action is most appropriate

        Examples of personal/memory questions (ALWAYS use 'respond with memory retrieval' for these):
        - "What is my favorite hobby?" (contains "my" and asks about personal preference)
        - "When is my next meeting?" (contains "my" and asks about personal schedule)
        - "What did I mention about..." (contains "I" and refers to past conversation)

        Examples of general knowledge questions (Use 'respond' for basic facts an AI would know):
        - "What is the largest ocean on Earth?" (basic geography)
        - "How many planets are in the solar system?" (basic science)
        - "What is the boiling point of water?" (common knowledge)
        - "What is the capital of France?" (basic geography)

        Only use 'research' for complex topics requiring detailed investigation or verification, like:
        - "What are the latest developments in quantum computing?"
        - "How has climate change affected migration patterns in Arctic birds?"
        - "What are the economic implications of recent policy changes?"

        IMPORTANT: ONLY use 'respond with memory retrieval' for questions that:
        1. Contain personal pronouns like "my", "I", "we"
        2. Ask about personal preferences, schedules, or past conversations
        3. Request information specific to the user

        For general knowledge, facts, or objective information, ALWAYS use 'respond'.

        Priority levels and their meanings:
        from frame.src.framer.agency.priority import Priority

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
        try:
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
            if isinstance(response, dict) and "error" in response:
                logger.warning(f"Error in LLM response: {response['error']}")
                return response
            return response
        except Exception as e:
            logger.error(f"Error in _get_decision_prompt: {str(e)}")
            return {
                "error": str(e),
                "fallback_response": "An error occurred while processing your request.",
            }

    async def execute_decision(
        self, decision: "Decision", perception: Optional[Perception] = None
    ) -> "Decision":
        """
        Execute the decision made by the brain.

        Args:
            decision (Decision): The decision to execute.
            perception (Optional[Perception]): The perception that led to this decision.

        Returns:
            Decision: The executed decision with results and status updated.
        """
        logger.debug(
            f"Executing decision: {decision.action} with params {decision.parameters}"
        )
        logger.debug(f"Perception object: {perception}")
        
        # Handle different execution modes
        if decision.execution_mode == ExecutionMode.AUTO:
            # Execute the action immediately
            result = await self.action_registry.execute_action(
                decision.action, **decision.parameters
            )
            decision.result = result
            decision.status = DecisionStatus.EXECUTED

        elif decision.execution_mode == ExecutionMode.USER_APPROVAL:
            # Handle user approval logic
            decision.status = DecisionStatus.PENDING_APPROVAL
            # Optionally, queue the decision for approval

        elif decision.execution_mode == ExecutionMode.DEFERRED:
            # Handle deferred execution logic
            decision.status = DecisionStatus.DEFERRED
            # Optionally, schedule the decision for later execution

        else:
            # Default to not executing
            decision.status = DecisionStatus.NOT_EXECUTED

        # Return the decision object with the result and status
        return decision

    async def _generate_new_query(self, decision: "Decision") -> str:
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