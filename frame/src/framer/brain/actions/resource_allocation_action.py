from frame.src.framer.brain.actions import BaseAction
from frame.src.framer.brain.strategies.decision_strategy import (
    DecisionStrategy,
    ConservativeStrategy,
    AggressiveStrategy,
    BalancedStrategy,
)
from frame.src.framer.brain.strategies.decision_strategy import (
    CollaborativeStrategy,
    InfluentialStrategy,
)
from frame.src.services.context.execution_context_service import ExecutionContext
from typing import Dict, Any

class ResourceAllocationAction(BaseAction):
    def __init__(self):
        super().__init__(
            "resource_allocation",
            "Allocate resources based on urgency, risk, and available resources.",
            priority=5,
        )
        self.strategies = {
            "conservative": ConservativeStrategy(),
            "aggressive": AggressiveStrategy(),
            "balanced": BalancedStrategy(),
            "collaborative": CollaborativeStrategy(),
            "influential": InfluentialStrategy(),
        }

    def choose_strategy(self, context: Dict[str, Any]) -> str:
        stakeholders = context.get("stakeholders", [])
        urgency = context.get("urgency", 0)

        if stakeholders and "high" in [s.get("influence", "low") for s in stakeholders]:
            return "influential"
        elif urgency < 3:
            return "conservative"
        elif stakeholders:
            return "collaborative"
        else:
            return "balanced"

    async def execute(self, execution_context: ExecutionContext, **kwargs: Any) -> Dict[str, Any]:
        context = execution_context.get_full_state()
        strategy_name = self.choose_strategy(context)
        strategy = self.strategies[strategy_name]
        decision = await strategy.decide(context)
        return decision

    def choose_strategy(self, context: Dict[str, Any]) -> str:
        urgency = context.get("urgency", 0)
        risk = context.get("risk", 0)
        resources = context.get("resources", "moderate")

        if urgency > 7 or (resources == "scarce" and risk > 5):
            return "aggressive"
        elif risk < 3 and resources == "abundant":
            return "conservative"
        else:
            return "balanced"

class StakeholderEngagementAction(BaseAction):
    def __init__(self):
        super().__init__(
            "stakeholder_engagement",
            "Engage with stakeholders based on their influence and the current context.",
            priority=5,
        )
        self.strategies = {
            "conservative": ConservativeStrategy(),
            "aggressive": AggressiveStrategy(),
            "balanced": BalancedStrategy(),
        }

    async def execute(self, execution_context: ExecutionContext, **kwargs: Any) -> Dict[str, Any]:
        context = execution_context.get_full_state()
        strategy_name = self.choose_strategy(context)
        strategy = self.strategies[strategy_name]
        decision = await strategy.decide(context)
        return decision

    def choose_strategy(self, context: Dict[str, Any]) -> str:
        stakeholders = context.get("stakeholders", [])
        urgency = context.get("urgency", 0)

        if stakeholders and "high" in [s.get("influence", "low") for s in stakeholders]:
            return "aggressive"
        elif urgency < 3:
            return "conservative"
        else:
            return "balanced"
