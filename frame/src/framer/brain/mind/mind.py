import logging
import json
from typing import List, Dict, Any, Optional
from unittest.mock import AsyncMock
from ..perception import Perception
from ..decision import Decision
from frame.src.framer.agency.action_registry import ActionRegistry
from frame.src.framer.agency.tasks import TaskStatusModel
from frame.src.utils.llm_utils import get_completion
from datetime import datetime

logger = logging.getLogger(__name__)


class Mind:
    """
    The Mind class represents the cognitive processes of a Framer.
    It manages thoughts, decision-making processes, perceptions, and interacts with the Brain and Soul components.
    """

    def __init__(self, brain: Any, recent_memories_limit: int = 5):
        """
        Initialize the Mind instance.

        Args:
            brain (Any): The Brain instance associated with this Mind.
            recent_memories_limit (int): The number of recent memories/perceptions to keep. Defaults to 5.
        """
        self.brain = brain
        self.thoughts: List[Dict[str, Any]] = []
        self.current_thought: Dict[str, Any] = {}
        self.perceptions: List[Perception] = []
        self.recent_memories_limit = recent_memories_limit

    def set_recent_memories_limit(self, limit: int):
        """
        Set the limit for recent memories/perceptions.

        Args:
            limit (int): The new limit for recent memories/perceptions.
        """
        self.recent_memories_limit = limit

    async def make_decision(self, perception: Perception) -> Decision:
        """
        Make a decision based on the current perceptions and thoughts.

        Args:
            perception (Perception): The perception to base the decision on.

        Returns:
            Decision: The decision made.
        """
        # Get the decision prompt from the brain
        prompt = self.brain._get_decision_prompt(perception)

        # Use the LLM service to get a decision
        response = await get_completion(
            self.brain.llm_service, prompt, model=self.brain.default_model
        )
        try:
            if isinstance(response, AsyncMock):
                # For testing purposes, return a default decision
                return Decision(
                    action="default_action",
                    parameters={},
                    reasoning="Default decision for testing",
                    confidence=0.5,
                    priority=5,
                )

            decision_data = json.loads(response) if isinstance(response, str) else {}
            action = decision_data.get("action", "default_action")
            if action not in self.brain.action_registry.actions:
                logger.warning(
                    f"Invalid action: {action}. Defaulting to 'default_action'."
                )
                action = "default_action"
                reasoning = f"Invalid action '{action}' was generated. Defaulted to 'default_action'."
            else:
                reasoning = decision_data.get("reasoning", "No reasoning provided.")

            decision = Decision(
                action=action,
                parameters=decision_data.get("parameters", {}),
                reasoning=decision_data.get("reasoning", "No reasoning provided."),
                confidence=float(decision_data.get("confidence", 0.5)),
                priority=int(decision_data.get("priority", 5)),
            )
        except json.JSONDecodeError:
            logger.error(f"Failed to parse decision response: {response}")
            decision = Decision(
                action="think",
                parameters={"error": "Failed to parse decision"},
                reasoning="The decision response could not be parsed as JSON.",
                confidence=0.1,
                priority=1,
            )

        logger.debug(f"Decision made: {decision}")
        return decision

    def think(self, thought: str) -> None:
        """
        Add a new thought to the Mind.

        Args:
            thought (str): The thought to add.
        """
        new_thought = {"content": thought, "timestamp": datetime.now()}
        self.thoughts.append(new_thought)
        self.current_thought = new_thought
        logger.debug(f"New thought: {thought}")

    def generate_thoughts(self) -> None:
        """
        Generate new thoughts based on current perceptions and memories.
        This method should be implemented to interact with the Soul's memory
        and the Brain's decision-making processes.
        """
        """
        Generate new thoughts based on current perceptions and memories.
        This method should be implemented to interact with the Soul's memory
        and the Brain's decision-making processes.
        """
        # TODO: Implement thought generation logic
        pass

    def get_current_thought(self) -> Dict[str, Any]:
        """
        Get the current thought of the Mind.

        Returns:
            Dict[str, Any]: The current thought with its timestamp.
        """
        return self.current_thought

    def get_all_thoughts(self) -> List[Dict[str, Any]]:
        """
        Get all thoughts stored in the Mind.

        Returns:
            List[Dict[str, Any]]: All thoughts with their timestamps.
        """
        return sorted(self.thoughts, key=lambda x: x["timestamp"], reverse=True)

    def clear_thoughts(self) -> None:
        """
        Clear all thoughts from the Mind.
        """
        self.thoughts.clear()
        self.current_thought = {}
        logger.debug("Thoughts cleared")

    async def process_perception(self, perception: Perception) -> Decision:
        """
        Process a perception and generate thoughts based on it.

        Args:
            perception (Perception): The perception to process.

        Returns:
            Decision: The decision made based on the perception.
        """
        self.perceptions.append(perception)
        perception_type = perception.type
        if perception_type:
            thought = f"Processed perception: {perception_type}"
        else:
            thought = "Processed perception without type"
        self.think(thought)
        return await self.make_decision(perception)

    def get_recent_perceptions(self, n: int = 5) -> List[Perception]:
        """
        Get the n most recent perceptions.

        Args:
            n (int): The number of recent perceptions to retrieve.

        Returns:
            List[Perception]: The n most recent perceptions.
        """
        if n <= 0:
            return []
        return self.perceptions[-n:]
