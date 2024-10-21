from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List, Union, TYPE_CHECKING
from frame.src.framer.agency.tasks import TaskStatus

if TYPE_CHECKING:
    from frame.src.framer.agency.priority import Priority


class Decision(BaseModel):
    action: str = Field(..., description="The action to be taken")
    parameters: Dict[str, Any] = Field(
        default_factory=dict, description="Parameters for the action"
    )
    expected_results: List[Any] = Field(
        default_factory=list, description="The expected results of the decision"
    )
    reasoning: str = Field(..., description="Reasoning behind the decision")
    confidence: float = Field(
        default=0.7, ge=0, le=1, description="Confidence level of the decision"
    )
    priority: Union["Priority", int] = Field(
        default=None, description="Priority of the decision"
    )
    task_status: Optional["TaskStatus"] = Field(
        default=None, description="Status of the associated task"
    )

    def __init__(self, **data):
        super().__init__(**data)

    result: Optional[Dict[str, Any]] = Field(
        default=None, description="The result of executing the decision"
    )

    class Config:
        populate_by_name = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "action": self.action,
            "parameters": self.parameters,
            "expected_results": self.expected_results,
            "reasoning": self.reasoning,
            "confidence": self.confidence,
            "priority": self.priority,
            "task_status": self.task_status.value if self.task_status else None,
            "result": self.result,
        }
