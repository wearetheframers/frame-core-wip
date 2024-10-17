from pydantic import BaseModel, Field
from typing import List, Dict, Any

class Goal(BaseModel):
    id: str
    description: str
    priority: int = Field(default=5, ge=1, le=10)

class Goals(BaseModel):
    goal_list: List[Goal] = []

    def add_goal(self, goal: Goal):
        self.goal_list.append(goal)

    def remove_goal(self, goal_id: str):
        self.goal_list = [goal for goal in self.goal_list if goal.id != goal_id]

    def get_goals(self) -> List[Goal]:
        return self.goal_list

    def clear_goals(self):
        self.goal_list = []

    def update_goal(self, goal_id: str, updated_goal: Goal):
        for i, goal in enumerate(self.goal_list):
            if goal.id == goal_id:
                self.goal_list[i] = updated_goal
                break
