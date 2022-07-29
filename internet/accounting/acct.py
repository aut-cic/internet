from datetime import datetime, timedelta
from typing import Any

from sanic_ext.utils.typing import typing
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..model.radacct import RadiusAccount
from ..model.raddaily import RadiusDaily
from .usage import Usage


class AccountingService:
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

        usage_history = []
        usage: Usage = Usage()
        statement = select(RadiusDaily).where(
            RadiusDaily.username == username
            and RadiusDaily.create_date > datetime.now() + timedelta(days=-30)
        )
        for row in self.session.scalars(statement):
            usage_history.append(
                {
                    "discount": row.usage_original - row.usage_discount,
                    "usage": row.usage_discount,
                    "created_date": row.create_date,
                }
            )

            usage.daily += (
                row.usage_discount
                if row.create_date > datetime.now() + timedelta(days=-24)
                else 0
            )
            usage.weekly += (
                row.usage_discount
                if row.create_date > datetime.now() + timedelta(days=-7)
                else 0
            )
            usage += row.usage_discount

        usage_history.reverse()

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
        return row.RadiusAccount.username
