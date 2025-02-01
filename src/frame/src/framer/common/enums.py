from enum import Enum


class ExecutionMode(str, Enum):
    AUTO = "auto"
    USER_APPROVAL = "user_approval"
    DEFERRED = "deferred"


class DecisionStatus(str, Enum):
    EXECUTED = "executed"
    PENDING_APPROVAL = "pending_approval"
    DEFERRED = "deferred"
    NOT_EXECUTED = "not_executed"


class TaskStatus(str, Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELED = "CANCELED"
    FAILED = "FAILED"
