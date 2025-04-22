from dataclasses import dataclass
from enum import Enum


class CommandState(Enum):
    NEW = "NEW"
    UPDATED = "UPDATED"
    DELETED = "DELETED"


class ProcessingState(Enum):
    NONE = "NONE"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"


@dataclass
class Command:
    commandId: int
    state: CommandState
    data: dict


@dataclass
class CommandResponse:
    commandId: int
    status: str
    data: dict
