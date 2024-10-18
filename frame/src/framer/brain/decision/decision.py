from __future__ import annotations
import json
from pydantic import Field
from typing import Dict, Any, Optional, Union, List
from frame.src.models.framer.brain.decision.decision import Decision as DecisionModel
from frame.src.models.framer.agency.tasks import TaskStatus
from frame.src.framer.agency.priority import Priority
from frame.src.framer.agency.roles import Role, RoleStatus
from frame.src.framer.agency.goals import Goal, GoalStatus


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
        task_status (TaskStatus): The status of the associated task.
        related_roles (List[Role]): Roles related to this decision.
        related_goals (List[Goal]): Goals related to this decision.
    """

    expected_results: List[Any] = Field(
        default_factory=list, description="The expected results of the decision"
    )
    task_status: TaskStatus = Field(
        default=TaskStatus.PENDING, description="Status of the associated task"
    )
    related_roles: List[Role] = Field(
        default_factory=list, description="Roles related to this decision"
    )
    related_goals: List[Goal] = Field(
        default_factory=list, description="Goals related to this decision"
    )

    class Config:
        arbitrary_types_allowed = True

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
        task_status: TaskStatus = TaskStatus.PENDING,
        related_roles: List[Role] = None,
        related_goals: List[Goal] = None,
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
    def convert_priority(priority: Union[str, int, Priority]) -> Priority:
        """
        Convert a priority level from string, integer, or Priority enum to a Priority enum value.

        Args:
            priority (Union[str, int, Priority]): The priority level as a string, integer, or Priority enum.

        Returns:
            Priority: The priority level as a Priority enum.
        """
        if isinstance(priority, Priority):
            return priority
        if isinstance(priority, str):
            try:
                return Priority[priority.upper()]
            except KeyError:
                return Priority.MEDIUM
        if isinstance(priority, int):
            try:
                return Priority(priority)
            except ValueError:
                return Priority.MEDIUM
        return Priority.MEDIUM

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
            self.task_status = TaskStatus.COMPLETED
            return {"result": result, "error": None}
        except Exception as e:
            self.task_status = TaskStatus.FAILED
            return {"result": None, "error": str(e)}

    def add_related_role(self, role: Role) -> None:
        """
        Add a related role to the decision.

        Args:
            role (Role): The role to add to the related roles.
        """
        if role not in self.related_roles:
            self.related_roles.append(role)

    def add_related_goal(self, goal: Goal) -> None:
        """
        Add a related goal to the decision.

        Args:
            goal (Goal): The goal to add to the related goals.
        """
        if goal not in self.related_goals:
            self.related_goals.append(goal)

    def remove_related_role(self, role_id: str) -> None:
        """
        Remove a related role from the decision.

        Args:
            role_id (str): The ID of the role to remove from the related roles.
        """
        self.related_roles = [role for role in self.related_roles if role.id != role_id]

    def remove_related_goal(self, goal_name: str) -> None:
        """
        Remove a related goal from the decision.

        Args:
            goal_name (str): The name of the goal to remove from the related goals.
        """
        self.related_goals = [
            goal for goal in self.related_goals if goal.name != goal_name
        ]
