from dataclasses import dataclass
from enum import Enum


class CommandState(Enum):
    NEW = "NEW"
    UPDATED = "UPDATED"
    DELETED = "DELETED"


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
