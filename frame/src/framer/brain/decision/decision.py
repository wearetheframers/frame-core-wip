import json
from enum import Enum


class DecisionStatus(str, Enum):
    EXECUTED = "executed"
    PENDING_APPROVAL = "pending_approval"
    DEFERRED = "deferred"
    NOT_EXECUTED = "not_executed"


from enum import Enum
from enum import Enum
from pydantic import BaseModel, Field


class DecisionStatus(str, Enum):
    EXECUTED = "executed"
    PENDING_APPROVAL = "pending_approval"
    DEFERRED = "deferred"
    NOT_EXECUTED = "not_executed"


class DecisionStatus(str, Enum):
    EXECUTED = "executed"
    PENDING_APPROVAL = "pending_approval"
    DEFERRED = "deferred"
    NOT_EXECUTED = "not_executed"


class ExecutionMode(str, Enum):
    AUTO = "auto"
    USER_APPROVAL = "user_approval"
    DEFERRED = "deferred"


from typing import Dict, Any, Optional, Union, List
from frame.src.models.framer.brain.decision import Decision as DecisionModel
from frame.src.framer.agency.priority import Priority
from frame.src.framer.agency.roles import Role
from frame.src.framer.agency.goals import Goal
from frame.src.framer.agency.tasks import TaskStatus, Task

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from frame.src.framer.agency.roles import Role
    from frame.src.framer.agency.goals import Goal


class ExecutionMode(str, Enum):
    AUTO = "auto"
    USER_APPROVAL = "user_approval"
    DEFERRED = "deferred"


class Decision(DecisionModel):
    """
    Represents a decision made by the Brain component of a Framer.

    Attributes:
        action (str): The action to be taken.
        parameters (Dict[str, Any]): Parameters for the action.
        reasoning (str): The reasoning behind the decision.
        confidence (float): The confidence level of the decision.
        priority (int): The priority of the decision.
        status (DecisionStatus): The execution status of the decision.

    Notes:
        The Decision class now includes validation of action parameters to ensure
        that all necessary variables are present and correctly formatted. This
        validation helps prevent execution errors and enhances the reliability of
        the decision-making process.
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
        task_status (TaskStatus): The status of the associated task.
        related_roles (List[Role]): Roles related to this decision.
        related_goals (List[Goal]): Goals related to this decision.
    """

    is_executable: bool = Field(
        default=True,
        description="Indicates if the decision can be executed automatically",
    )
    execution_mode: ExecutionMode = Field(
        default=ExecutionMode.AUTO,
        description="Defines how the decision should be executed.",
    )
    execution_mode: ExecutionMode = Field(
        default=ExecutionMode.AUTO,
        description="Defines how the decision should be executed.",
    )
    execution_mode: str = Field(
        default="auto",
        description="Defines how the decision should be executed. Options: 'auto', 'user_approval', 'deferred'",
    )
    expected_results: List[Any] = Field(
        default_factory=list, description="The expected results of the decision"
    )
    status: DecisionStatus = Field(
        default=DecisionStatus.NOT_EXECUTED,
        description="The execution status of the decision",
    )
    status: DecisionStatus = Field(
        default=DecisionStatus.NOT_EXECUTED,
        description="The execution status of the decision",
    )
    status: DecisionStatus = Field(
        default=DecisionStatus.NOT_EXECUTED,
        description="The execution status of the decision",
    )
    task_status: TaskStatus = Field(
        default=TaskStatus.PENDING, description="Status of the associated task"
    )
    related_roles: List["Role"] = Field(
        default_factory=list, description="Roles related to this decision"
    )
    related_goals: List["Goal"] = Field(
        default_factory=list, description="Goals related to this decision"
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
            decision_dict = json_data
        else:
            decision_dict = json.loads(json_data)

        # Convert priority from string or integer to Priority enum
        from frame.src.framer.agency import Priority

        decision_dict["priority"] = Priority.from_value(
            decision_dict.get("priority", Priority.MEDIUM)
        )

        return cls(**decision_dict)

    def to_task(self) -> "Task":
        """
        Convert the Decision into a Task.
        """
        return Task(
            description=self.reasoning,
            priority=self.priority,
            status=TaskStatus.PENDING,
            data=self.parameters,
            type=self.action,
        )

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
            "execution_mode": self.execution_mode.value,
            "expected_results": self.expected_results,
            "task_status": self.task_status.value,
            "status": self.status.value,
            "related_roles": [
                role.to_dict() if hasattr(role, "to_dict") else str(role)
                for role in self.related_roles
            ],
            "related_goals": [
                goal.dict() if hasattr(goal, "dict") else str(goal)
                for goal in self.related_goals
            ],
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
        task_status: "TaskStatus" = None,
        related_roles: List["Role"] = None,
        related_goals: List["Goal"] = None,
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
            task_status (TaskStatus, optional): The status of the associated task. Defaults to PENDING.
            related_roles (List[Role], optional): Roles related to this decision. Defaults to None.
            related_goals (List[Goal], optional): Goals related to this decision. Defaults to None.

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
            related_roles=related_roles or [],
            related_goals=related_goals or [],
        )

    @staticmethod
    def convert_priority(priority: Union[str, int]) -> int:
        """
        Convert a priority level from string or integer to an integer value.

        Args:
            priority (Union[str, int]): The priority level as a string or integer.

        Returns:
            int: The priority level as an integer.
        """
        if isinstance(priority, int):
            return priority
        if isinstance(priority, str):
            try:
                return Priority[priority.upper()].value
            except KeyError:
                raise ValueError(f"Invalid priority level: {priority}")
        raise ValueError("Priority must be a string or Priority enum")

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
            f"task_status={self.task_status.value}, "
            f"related_roles={len(self.related_roles)}, "
            f"related_goals={len(self.related_goals)})"
        )

    class Config:
        arbitrary_types_allowed = True


Decision.update_forward_refs()
