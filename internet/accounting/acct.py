from typing import Any


def user_usage(ip: str) -> Any:
    response = {
        "resetConfig": {"daily": 0, "monthly": 0, "weekly": 0},
        "speeds": {"monthly": "1M/2M"},
        "groupname": "",
        "package": {"daily": 0, "monthly": 0, "weekly": 0, "free": 0},
        "usage": {"daily": 0, "monthly": 0, "weekly": 0},
        "sessions": [],
        "usagehistory": [],
        "username": "",
    }

    return response


def radius_usage(ip: str):
    pass
