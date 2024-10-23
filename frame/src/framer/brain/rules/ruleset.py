from typing import Callable, List, Dict, Any


class Rule:
    def __init__(
        self,
        condition: Callable[[Dict[str, Any]], bool],
        action: Callable[[Dict[str, Any]], None],
    ):
        self.condition = condition
        self.action = action

    def evaluate(self, context: Dict[str, Any]) -> bool:
        return self.condition(context)

    def execute(self, context: Dict[str, Any]) -> None:
        if self.evaluate(context):
            self.action(context)


class Ruleset:
    def __init__(self):
        self.rules: List[Rule] = []

    def add_rule(self, rule: Rule) -> None:
        self.rules.append(rule)

    def evaluate(self, context: Dict[str, Any]) -> None:
        for rule in self.rules:
            rule.execute(context)
