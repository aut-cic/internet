import dataclasses
import datetime


@dataclasses.dataclass
class UsageRecord:
    """
    daily records based on what we have on radius database,
    this used as a basis for generating other reports.
    """

    discount: int
    usage: int
    created_date: datetime.date


@dataclasses.dataclass
class Session:
    """
    each session is a successful login.
    """

    ip: str
    id: str
    time: datetime.datetime
    usage: str
    location: str
    is_current: bool


@dataclasses.dataclass
class Usage:
    """
    usage is aggregated download/upload in the last month in bytes.
    """

    daily: int = 0
    weekly: int = 0
    monthly: int = 0


@dataclasses.dataclass
class Package:
    """
    package specify the available download/upload volume
    based on your group name in GB.
    """

    daily_volume: int = 0
    weekly_volume: int = 0
    monthly_volume: int = 0


@dataclasses.dataclass
class Report:
    """
    aggregated information for generating the status page.
    """

    usage_history: list[UsageRecord]
    package: Package
    groupname: str
    usage: Usage
    username: str
    sessions: list[Session]
