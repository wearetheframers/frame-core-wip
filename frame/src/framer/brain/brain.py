import json
import logging
import re
from typing import Any, Dict, List, Optional, Union, Callable

logger = logging.getLogger(__name__)

from frame.src.utils.llm_utils import get_llm_provider
from frame.src.services import ExecutionContext, LLMService
from frame.src.models.framer.brain.decision.decision import Decision
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
        execution_context: Optional["ExecutionContext"] = None,
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
        self.logger.info("Initializing Brain")
        self.llm_service = llm_service
        self.execution_context = execution_context or ExecutionContext(
            llm_service=self.llm_service
        )
        self.default_model = default_model
        self.roles = roles
        self.goals = goals
        self.soul = soul
        self.memory_service = memory_service
        self.logger.info(f"Memory service received: {self.memory_service}")

        if self.memory_service:
            self.logger.info("Creating Memory object")
            self.memory = Memory(self.memory_service)
            self.logger.info(f"Memory object created: {self.memory}")
        else:
            self.logger.warning("No memory service provided, Memory object not created")
            self.memory = None

        self.mind = Mind(self)
        # Initialize ActionRegistry
        self.action_registry = ActionRegistry(execution_context=self.execution_context)
        if not isinstance(self.execution_context, ExecutionContext):
            raise TypeError("execution_context must be an instance of ExecutionContext")

        self.logger.info(
            f"Brain initialized with memory service: {self.memory_service}"
        )
        self.logger.info(f"Brain memory object: {self.memory}")

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

    def set_framer(self, framer):
        self.framer = framer
        self.action_registry.set_execution_context(self.execution_context)

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
            await self.llm_service.get_completion(
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
            return {
                "action": "error",
                "parameters": {
                    "error": "Received None response",
                    "raw_response": str(response),
                },
                "reasoning": "Failed to parse the decision data due to None response.",
                "confidence": 0.0,
                "priority": 1,
            }

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

        self.mind.perceptions.append(perception)
        available_actions = self.action_registry.get_all_actions().keys()
        self.logger.debug(f"Processing perception: {perception}")
        self.logger.debug(f"Avaliable actions: {available_actions}")
        decision = await self.make_decision(perception)
        if hasattr(self, "framer") and getattr(self.framer, "can_execute", False):
            if decision is None:
                self.logger.warning("No decision was made for the given perception.")
                return None
            result = await self.execute_decision(decision, perception)
            return result
        else:
            logger.warn("Framer is not ready to execute decisions. Queuing perception.")
            # Code to queue the perception can be added here if needed
        return decision

    async def make_decision(
        self, perception: Optional[Perception] = None
    ) -> "Decision":
        from frame.src.framer.brain.decision import Decision

        """
        Make a decision on what action to take next based on the current state and perception.

        Args:
            perception (Optional[Perception]): The current perception of the environment.

        Returns:
            Decision: The decision made based on the current state and perception,
                      including the action to take, parameters, reasoning, confidence,
                      and priority.
        """
        logger.info(f"Making decision based on perception: {perception}")
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

        decision_data = self.parse_json_response(response)

        logger.info(f"Decision data received: {decision_data}")

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

        action = decision_data.get("action", "respond").lower()
        valid_actions = [
            str(action).lower()
            for action in self.action_registry.get_all_actions().keys()
        ]

        # Check if the action is valid
        if action not in valid_actions:
            # If the action is not valid, check if it's related to memory retrieval
            if any(keyword in action for keyword in ["memory", "recall", "retrieve"]):
                action = "respond with memory retrieval"
                decision_data["action"] = action
                decision_data["reasoning"] = (
                    f"Action '{action}' was generated based on the perception. "
                    f"Using the memory retrieval plugin to process this request."
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

        logger.info(f"Decision data generated: {decision_data}")
        logger.info(f"Action '{action}' generated: {decision_data}")

        parameters = decision_data.get("parameters", {})
        if action == "respond with memory retrieval" and "query" not in parameters:
            parameters["query"] = perception.data.get("text", "")
        elif "topic" in parameters:
            parameters["research_topic"] = parameters.pop("topic")
        if not isinstance(parameters, dict):
            parameters = {"value": parameters}

        reasoning = decision_data.get("reasoning", "No reasoning provided.")

        # Check if goals are None and generate them if necessary
        if self.execution_context and not self.execution_context.get_goals():
            # Assuming the execution_context has a method to generate goals
            goals = await self.execution_context.generate_goals()
            self.execution_context.set_goals(goals)

        # Consider role and goal priorities when setting decision priority
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
        priority_value = None
        priority_int = None
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
        logger.info(f"Final decision object: {decision}")
        logger.info(f"Decision made: {decision}")
        if hasattr(decision, "reasoning"):
            decision.reasoning += f" (Aligned with {len(active_goals)} active goals)"
        else:
            logger.error("Decision object does not have a 'reasoning' attribute.")
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

        Valid actions are:
        {json.dumps({str(action): f"{self.action_registry.actions[action]['description']} (Priority: {self.action_registry.actions[action]['priority']})" for action in self.action_registry.actions}, indent=2)}
        
        For each perception, carefully evaluate:
        - The type and content of the perception
        - The urgency and importance of the information
        - The current active goals and roles of the system, considering their priorities and statuses
        - Whether immediate action, further research, or no action is most appropriate

        Examples of personal/memory questions (ALWAYS use 'respond with memory retrieval' for these):
        - "What is my favorite hobby?"
        - "When is my next meeting?"
        - "What did I mention about my travel plans?"

        Examples of general knowledge questions (use 'respond' for these):
        - "What is the largest ocean on Earth?"
        - "How many planets are in the solar system?"
        - "What is the freezing point of water in Fahrenheit?"

        IMPORTANT: For ANY question that seems to require personal information or memory, ALWAYS choose the 'respond with memory retrieval' action. This includes questions about appointments, preferences, past conversations, or any user-specific information.

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
    ):
        from frame.src.framer.brain.decision import Decision

        """
        Execute the decision made by the brain.

        Args:
            decision (Decision): The decision to execute.
            perception (Optional[Perception]): The perception that led to this decision.
        """
        logger.info(
            f"Executing decision: {decision.action} with params {decision.parameters}"
        )
        result = None
        try:
            if decision.action not in self.action_registry.get_all_actions():
                logger.warning(
                    f"Action '{decision.action}' not found in registry. Defaulting to 'process_perception'."
                )
                decision.action = "process_perception"
                if "perception" not in decision.parameters:
                    decision.parameters["perception"] = (
                        perception.data if perception else None
                    )

            if decision.action == "respond with memory retrieval":
                if (
                    "query" not in decision.parameters
                    or not decision.parameters["query"]
                ):
                    decision.parameters["query"] = (
                        perception.data.get("text", "") if perception else ""
                    )

            result = await self.action_registry.execute_action(
                decision.action, decision.parameters
            )

            logger.info(
                f"Action result: {result} with reasoning: {decision.reasoning}."
            )

        except Exception as e:
            logger.error(f"Error executing decision: {e}")
            logger.exception("Detailed traceback:")
            result = {"error": str(e)}

        return result

    async def execute_action(self, action_name: str, parameters: dict):
        """Execute an action by its name using the action registry."""
        return await self.action_registry.execute_action(action_name, parameters)

    async def _execute_decision(self, decision: Decision) -> Any:
        """
        Execute the decision made by the brain.

        Args:
            decision (Decision): The decision to execute.

        Returns:
            Any: The result of executing the decision.
        """
        logger.debug(f"Executing decision: {decision.action}")
        logger.debug(f"Decision parameters: {decision.parameters}")
        result = None
        try:
            # Pass priorities to the LLM to help prioritize tasks based on relevance
            for (
                action_name,
                action_info,
            ) in self.action_registry.get_all_actions().items():
                if action_name == decision.action:
                    if action_name == "think":
                        result = await self._execute_think_action(decision)
                    elif action_name == "respond":
                        result = await self.perform_task(
                            {
                                "description": decision.parameters.get("content", ""),
                                "workflow_id": "default",
                            }
                        )
                    else:
                        print(f"Executing action: {action_name}")
                        print("Action info: ", action_info)
                        try:
                            result = await self.action_registry.execute_action(
                                action_name, decision.parameters
                            )
                        except Exception as e:
                            logger.error(f"Error executing action '{action_name}': {e}")
                            result = {
                                "error": str(e),
                                "fallback_response": "An error occurred while processing your request. Please try again.",
                            }
                    break
            else:
                raise ValueError(f"Action '{decision.action}' not found in registry.")

            logger.info(f"Executed action: {decision.action}")
            logger.debug(f"Action result: {result}")
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
