from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any

from sanic_ext.utils.typing import typing
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..model.radacct import RadiusAccount
from ..model.raddaily import RadiusDaily
from ..model.radpackages import RadiusPackages
from ..model.radusergroup import RadiusUserGroup
from .usage import Package, Report
from .usage import Session as IESession
from .usage import Usage, UsageRecord


class AccountingService:
    """
    AccountingService does all accounting things.
    """

    def __init__(self, session: Session):
        self.session = session

    def user_usage(self, username: str) -> Report:
        """
        aggregate information from free radius database.
        please note that group name may contain -H1, -H2 and -H3
        to show that your current usage type.
        """
        # usage and usage_history from radius daily table
        usage_history: list[UsageRecord] = []
        usage: Usage = Usage()
        statement = (
            select(RadiusDaily)
            .where(RadiusDaily.username == username)
            .where(
                RadiusDaily.create_date
                > (datetime.now() + timedelta(days=-30)).date()
            )
        )
        for row in self.session.scalars(statement):
            usage_history.append(
                UsageRecord(
                    discount=row.usage_original - row.usage_discount,
                    usage=row.usage_discount,
                    created_date=row.create_date,
                )
            )

            usage.daily += (
                row.usage_discount
                if row.create_date
                > (datetime.now() + timedelta(days=-24)).date()
                else 0
            )
            usage.weekly += (
                row.usage_discount
                if row.create_date
                > (datetime.now() + timedelta(days=-7)).date()
                else 0
            )
            usage.monthly += row.usage_discount

        usage.free = usage.monthly
        usage_history.reverse()

        # sessions from radius account table
        sessions: list[IESession] = []
        statement = (
            select(RadiusAccount)
            .where(RadiusAccount.username == username)
            .where(RadiusAccount.account_stop_time is None)
        )
        for row in self.session.scalars(statement):
            sessions.append(
                IESession(
                    ip=row.framedipaddress,
                    id=row.account_unique_id,
                    time=row.account_start_time,
                    usage=row.account_input_octets + row.account_output_octets,
                    # location information must calculate
                    # based on ip address.
                    location="-",
                    is_current=False,
                )
            )

        # user's groupname
        group_name = ""
        package: Package = Package()
        statement = select(RadiusUserGroup).where(
            RadiusUserGroup.username == username
        )
        row = self.session.scalars(statement).first()
        if row is not None:
            group_name = row.group_name
            # gather packages for the group
            statement = select(RadiusPackages).where(
                RadiusPackages.group_name
                == group_name.split("-", maxsplit=1)[0]
            )
            row = self.session.scalars(statement).first()
            if row is not None:
                package = Package(
                    daily_volume=row.daily_volume,
                    weekly_volume=row.weekly_volume,
                    monthly_volume=row.monthly_volume,
                    free_volume=4 * row.monthly_volume,
                )

        return Report(
            username=username,
            usage_history=usage_history,
            usage=usage,
            sessions=sessions,
            groupname=group_name,
            package=package,
        )

    def ip_to_username(self, ip: str) -> str | None:
        """
        in internet service we only has user ip address because they are only
        using microtik for login and etc.
        please note that ip 127.0.0.1 is use only for testing purpose so
        I return my username.
        """
        if ip == "127.0.0.1":
            return "parham.alvani"

        statement = (
            select(RadiusAccount.username)
            .where(RadiusAccount.framedipaddress == ip)
            .where(RadiusAccount.account_stop_time is None)
        )
        row = self.session.execute(statement).first()
        if row is None:
            return None
        return row.RadiusAccount.username
