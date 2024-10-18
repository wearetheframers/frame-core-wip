from typing import List
from frame.src.models.framer.agency.goals import Goal, GoalStatus
from frame.src.models.framer.agency.priority import Priority


class Goals:
    """
    Manages a list of goals for a Framer.
    Multiple goals can be active at the same time.

    This class provides methods to add, remove, evaluate, and manage goals.
    It allows for dynamic goal management within the Framer's agency.

    Attributes:
        goals (List[Goal]): A list of Goal objects representing the current goals.
    """

    def __init__(self):
        self.goals: List[Goal] = []

    def add_goal(self, goal: Goal):
        """
        Add a new goal to the list.

        The goal will be active by default.

        Args:
            goal (Goal): The goal to be added.
        """
        if isinstance(goal.priority, str):
            goal.priority = Priority.from_string(goal.priority)
        elif not isinstance(goal.priority, Priority):
            goal.priority = Priority.MEDIUM
        self.goals.append(goal)

    def remove_goal(self, goal_name: str):
        """
        Remove a goal from the list based on its name.

        Args:
            goal_name (str): The name of the goal to be removed.
        """
        self.goals = [goal for goal in self.goals if goal.name != goal_name]

    def evaluate_goals(self):
        """
        Evaluate and possibly update goal priorities.

        This method can be implemented to adjust priorities based on current context.
        It's a placeholder for more complex goal evaluation logic.
        """
        pass

    def set_goal_status(self, goal_name: str, status: GoalStatus):
        """
        Set the status of a specific goal.

        Multiple goals can be active simultaneously.

        Args:
            goal_name (str): The name of the goal to update.
            status (GoalStatus): The new status to set for the goal.
        """
        for goal in self.goals:
            if goal.name == goal_name:
                goal.status = status
                break

    def get_active_goals(self) -> List[Goal]:
        """
        Retrieve all currently active goals.

        Returns:
            List[Goal]: A list of all goals with an ACTIVE status.
        """
        return [goal for goal in self.goals if goal.status == GoalStatus.ACTIVE]

    def prioritize_goals(self):
        """
        Adjust the priorities of goals based on current context or performance.

        This method can be implemented to dynamically update goal priorities.
        """
        # Implement prioritization logic here
        pass
