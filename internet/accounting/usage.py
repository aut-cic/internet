import dataclasses


@dataclasses.dataclass
class Sesssion:
    ip: str
    time: str
    usage: str
    id: str
    location: str
    is_current: bool


@dataclasses.dataclass
class Usage:
    packages: dict[str, int]
    groupname: str
    usage: dict[str, int]
    username: str
    sessions: list[Sesssion]
