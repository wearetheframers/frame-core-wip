from frame.src.models.framer.agency.goals import Goals, Goal, GoalStatus as GoalsModel, GoalModel, GoalStatusModel

class Goals(GoalModel):
    """
    Manages a list of goals for a Framer.
    Multiple goals can be active at the same time.
    """
    goal_list: list[Goal] = []

    def add_goal(self, goal: Goal):
        """Add a new goal. The goal will be active by default."""
        self.goal_list.append(goal)

    def remove_goal(self, goal_name: str):
        self.goal_list = [goal for goal in self.goal_list if goal.name != goal_name]

    def evaluate_goals(self):
        """
        Evaluate and possibly update goal priorities.
        This method can be implemented to adjust priorities based on current context.
        """
        pass

    def set_goal_status(self, goal_name: str, status: GoalStatusModel):
        """Set the status of a goal. Multiple goals can be active simultaneously."""
        for goal in self.goal_list:
            if goal.name == goal_name:
                goal.status = status
                break