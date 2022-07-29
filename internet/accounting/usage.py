import dataclasses
import datetime
import enum
import math

# http://stackoverflow.com/questions/10420352
__units = [
    "کیلوبایت",
    "مگابایت",
    "گیگابایت",
    "ترابایت",
    "پتا بایت",
    #    "EiB",
    #    "ZiB",
    #    "YiB",
]


def bytes_to_str(bytes: float) -> str:
    """
    convert bytes into human readable format with unit.
    """
    threshold = 1024

    if math.isnan(bytes):
        return "∞"

    if math.fabs(bytes) < threshold:
        return "-"

    units_index = -1

    while math.fabs(bytes) >= threshold and units_index < len(__units):
        bytes /= threshold
        units_index += 1

    if units_index < 2 or ((bytes * 10) % 10) == 0:
        return f"{bytes:.0f} {__units[units_index]}"

    return f"{bytes:.1f} {__units[units_index]}"


class UsageType(enum.Enum):
    """
    different types of usage which has their
    specific field in reports.
    """

    DAILY = 1
    WEEKLY = 2
    MONTHLY = 3
    FREE = 4

    def __str__(self) -> str:
        return self.name.lower()


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
    usage: int
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
    free: int = 0


@dataclasses.dataclass
class Package:
    """
    package specify the available download/upload volume
    based on your group name in GB.
    """

    daily_volume: int = 0
    weekly_volume: int = 0
    monthly_volume: int = 0
    free_volume: int = 0


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

    def get_active_type(self) -> UsageType:
        """
        user active package is specify by group name prefix.
        """
        match self.groupname.split("-"):
            case [_, "H1"]:
                return UsageType.WEEKLY
            case [_, "H2"]:
                return UsageType.MONTHLY
            case [_, "H3"]:
                return UsageType.FREE
            case _:
                return UsageType.DAILY
