from pydantic import BaseModel
from typing import List, Dict, Any


class Goal(BaseModel):
    name: str
    description: str
    priority: int


class Goals(BaseModel):
    goal_list: List[Goal] = []

    def add_goal(self, goal: Goal):
        self.goal_list.append(goal)

    def remove_goal(self, goal_name: str):
        self.goal_list = [goal for goal in self.goal_list if goal.name != goal_name]

    def evaluate_goals(self) -> List[Goal]:
        # Implement evaluation logic here
        return self.goal_list
