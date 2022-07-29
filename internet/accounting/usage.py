import dataclasses
import datetime


@dataclasses.dataclass
class Session:
    ip: str
    time: datetime.datetime
    usage: str
    id: str
    location: str
    is_current: bool


@dataclasses.dataclass
class Usage:
    daily: int = 0
    weekly: int = 0
    monthly: int = 0


@dataclasses.dataclass
class Report:
    packages: dict[str, int]
    groupname: str
    usage: Usage
    username: str
    sessions: list[Session]
