import dataclasses
import datetime


@dataclasses.dataclass
class UsageRecord:
    discount: int
    usage: int
    created_date: datetime.date


@dataclasses.dataclass
class Session:
    ip: str
    id: str
    time: datetime.datetime
    usage: str
    location: str
    is_current: bool


@dataclasses.dataclass
class Usage:
    daily: int = 0
    weekly: int = 0
    monthly: int = 0


@dataclasses.dataclass
class Package:
    daily_volume: int = 0
    weekly_volume: int = 0
    monthly_volume: int = 0


@dataclasses.dataclass
class Report:
    usage_history: list[UsageRecord]
    package: Package
    groupname: str
    usage: Usage
    username: str
    sessions: list[Session]
