from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..model.radacct import RadiusAccount


class Usage:
    def __init__(self, session: Session):
        self.session = session

    def user_usage(self, username: str) -> Any:
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

    def ip_to_username(self, ip: str) -> str | None:
        """
        in internet service we only has user ip address because they are only
        using microtik for login and etc.
        """
        statement = select(RadiusAccount.username).where(
            RadiusAccount.framedipaddress == ip
            and RadiusAccount.account_stop_time is None
        )
        row = self.session.execute(statement).first()
        if row is None:
            return None
        return row.username
