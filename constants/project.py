from enum import Enum, StrEnum, unique


@unique
class Priority(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@unique
class Status(StrEnum):
    ACTIVE = "active"
    DEPLOYED = "deployed"
    HOLD = "hold"
    INACTIVE = "inactive"
    COMPLETED = "completed"
    RISK = "risk"
