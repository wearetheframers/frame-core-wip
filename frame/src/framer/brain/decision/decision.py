import json
from pydantic import Field
from typing import Dict, Any, Optional, Union, List
from frame.src.models.framer.brain.decision.decision import Decision as DecisionModel
from frame.src.models.framer.agency.tasks.task import TaskStatus


class Decision(DecisionModel):
    """
    Represents a decision made by the Brain component of a Framer.

    To extend decision-making capabilities, you can add new actions to the
    ActionRegistry and ensure they are recognized in the decision-making process.

    Attributes:
        action (str): The action to be taken.
        parameters (Dict[str, Any]): Parameters for the action.
        reasoning (str): The reasoning behind the decision.
        confidence (float): The confidence level of the decision.
        priority (int): The priority of the decision.
        expected_results (Optional[Any]): The expected results of the decision.
        task_status (TaskStatusModel): The status of the associated task.
    """

    expected_results: List[Any] = Field(
        default_factory=list, description="The expected results of the decision"
    )
    task_status: TaskStatus = Field(
        default=TaskStatus.PENDING, description="Status of the associated task"
    )

    @classmethod
    def from_json(cls, json_data: Union[str, Dict[str, Any]]) -> "Decision":
        """
        Create a Decision instance from a JSON string or dictionary.

        Args:
            json_str (str or dict): JSON string or dictionary representing a Decision.

        Returns:
            Decision: An instance of the Decision class.
        """
        if isinstance(json_data, dict):
            return cls(**json_data)
        decision_dict = json.loads(json_data)
        return cls(**decision_dict)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the Decision object to a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the Decision.
        """
        return {
            "action": self.action,
            "parameters": self.parameters,
            "reasoning": self.reasoning,
            "confidence": self.confidence,
            "priority": self.priority,
            "expected_results": self.expected_results,
            "task_status": self.task_status.value,
        }

    @classmethod
    def create(
        cls,
        action: str,
        parameters: Dict[str, Any],
        reasoning: str,
        confidence: float = 0.7,
        priority: int = 5,
        expected_results: Optional[Any] = None,
        task_status: TaskStatus = TaskStatus.PENDING,
    ) -> "Decision":
        """
        Create a new Decision instance with the given parameters.

        Args:
            action (str): The action to be taken.
            parameters (Dict[str, Any]): Parameters for the action.
            reasoning (str): The reasoning behind the decision.
            confidence (float, optional): The confidence level of the decision. Defaults to 0.7.
            priority (int, optional): The priority of the decision on a scale from 1 (lowest) to 10 (highest). Defaults to 5.
            expected_results (Optional[Any], optional): The expected results of the decision. Defaults to None.
            task_status (TaskStatusModel, optional): The status of the associated task. Defaults to PENDING.

        Returns:
            Decision: A new Decision instance.
        """
        return cls(
            action=action,
            parameters=parameters,
            reasoning=reasoning,
            confidence=confidence,
            priority=priority,
            expected_results=expected_results,
            task_status=task_status,
        )

    def update_status(self, new_status: TaskStatus) -> None:
        """
        Update the task status of the decision.

        Args:
            new_status (TaskStatusModel): The new status to set.
        """
        self.task_status = new_status

    def __str__(self) -> str:
        """
        Return a string representation of the Decision.

        Returns:
            str: A string representation of the Decision.
        """
        return (
            f"Decision(action={self.action}, "
            f"confidence={self.confidence:.2f}, "
            f"priority={self.priority}, "
            f"task_status={self.task_status.value})"
        )

    async def execute(self, action_registry: Any) -> Dict[str, Any]:
        """
        Execute the decision using the provided action registry.

        Args:
            action_registry (Any): The action registry containing available actions.

        Returns:
            Dict[str, Any]: The result of executing the action.
        """
        if self.action not in action_registry.actions:
            raise ValueError(f"Action '{self.action}' not found in action registry")

        action_func = action_registry.actions[self.action]["action_func"]
        try:
            result = await action_func(**self.parameters)
            return {"result": result, "error": None}
        except Exception as e:
            return {"result": None, "error": str(e)}
