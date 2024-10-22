from frame.src.framer.brain.actions import BaseAction
from frame.src.framer.brain.actions.strategies.decision_strategy import (
    DecisionStrategy,
    ConservativeStrategy,
    AggressiveStrategy,
    BalancedStrategy,
)
from frame.src.services import ExecutionContext
from typing import Dict, Any


class AdaptiveDecisionAction(BaseAction):
    def __init__(self):
        super().__init__(
            name="adaptive_decision",
            description="A high-level action that uses strategies to make decisions dynamically based on varying levels of urgency and risk. "
                        "Ideal for environments where conditions change rapidly, requiring a flexible decision-making approach. "
                        "Examples include financial trading during volatile markets, task prioritization in dynamic project environments, "
                        "or resource allocation in cloud computing under fluctuating demand.",
            priority=5,
        )
        self.strategies = {
            "conservative": ConservativeStrategy(),
            "aggressive": AggressiveStrategy(),
            "balanced": BalancedStrategy(),
        }

    async def execute(
        self, execution_context: ExecutionContext, **kwargs: Any
    ) -> Dict[str, Any]:
        # Determine the best strategy based on the context
        context = execution_context.get_full_state()
        context = self.extrapolate_context(context)
        strategy_name = self.choose_strategy(context)
        strategy = self.strategies[strategy_name]
        decision = await strategy.decide(context)
        return {"decision": decision, "strategy": strategy_name}

    def extrapolate_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extrapolate missing context data to ensure robust decision-making.
        """
        if "urgency" not in context or "risk" not in context:
            # Use historical data or default values to estimate urgency and risk
            context["urgency"] = context.get("historical_urgency", 5)
            context["risk"] = context.get("historical_risk", 5)

        # If perception data is available, use it to refine urgency and risk
        perception_data = context.get("perception_data", {})
        if perception_data:
            context["urgency"] = perception_data.get("urgency", context["urgency"])
            context["risk"] = perception_data.get("risk", context["risk"])

        # Ensure all necessary context keys are present
        context.setdefault("resources", "moderate")
        context.setdefault("stakeholders", [])
        context.setdefault("deadline", None)
        context.setdefault("dependencies", [])
        context.setdefault("external_factors", [])

        return context

    def choose_strategy(self, context: Dict[str, Any]) -> str:
        # Logic to choose the best strategy based on context
        urgency = context.get("urgency", 0)
        risk = context.get("risk", 0)
        resources = context.get("resources", "moderate")
        stakeholders = context.get("stakeholders", [])
        deadline = context.get("deadline", None)
        dependencies = context.get("dependencies", [])
        external_factors = context.get("external_factors", [])

        # Example logic considering multiple factors, including extrapolated data
        if urgency > 7 or (resources == "scarce" and risk > 5):
            return "aggressive"
        elif risk < 3 and resources == "abundant":
            return "conservative"
        elif stakeholders and any(s in stakeholders for s in ["team G"]):
            return "balanced"
        elif deadline and risk > 5 and deadline < "2025-01-01":
            return "aggressive"
        elif dependencies and "project Z" in dependencies:
            return "balanced"
        elif "technological advancements" in external_factors:
            return "balanced"
        else:
            return "conservative"
