from frame.src.framer.brain.actions import BaseAction
from frame.src.framer.agency.roles import Role, RoleStatus
from frame.src.framer.agency.goals import Goal, GoalStatus
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from frame.src.framer.agency import RoleStatus, GoalStatus


class ErrorAction(BaseAction):
    def __init__(self):
        super().__init__(
            name="error",
            description="Handle errors by apologizing and attempting to continue the conversation.",
            priority=1,
        )

    async def execute(self, execution_context, **kwargs):
        error_message = kwargs.get("error", "An unknown error occurred.")
        soul_state = (
            execution_context.soul.get_current_state()
            if execution_context and execution_context.soul
            else "No soul state available."
        )
        recent_thoughts = (
            execution_context.get_recent_thoughts()[-5:]
            if execution_context and hasattr(execution_context, "get_recent_thoughts")
            else []
        )
        active_roles = (
            [
                role.name
                for role in execution_context.roles
                if isinstance(role, Role) and role.status == RoleStatus.ACTIVE
            ]
            if execution_context and hasattr(execution_context, "roles")
            else []
        )
        active_goals = (
            [
                goal.name
                for goal in execution_context.get_goals()
                if isinstance(goal, Goal) and goal.status == GoalStatus.ACTIVE
            ]
            if execution_context and hasattr(execution_context, "get_goals")
            else []
        )

        response = (
            f"I apologize, an error occurred: {error_message}. "
            "Let's try to continue our conversation.\n\n"
            "### Current Framer State\n"
            f"- Soul State: {soul_state}\n"
            f"- Recent Thoughts: {recent_thoughts}\n"
            f"- Active Roles: {active_roles}\n"
            f"- Active Goals: {active_goals}\n"
        )
        return {"response": response}
