"""
accouting servier source file.
this service used for accessing free-radius database
to manage account and usage.
"""
from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..model.radacct import RadiusAccount
from ..model.raddaily import RadiusDaily
from ..model.radpackages import RadiusPackages
from ..model.radusergroup import RadiusUserGroup
from ..subnets import lookup
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
                > (datetime.now() + timedelta(days=-1)).date()
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
            .where(RadiusAccount.account_stop_time == None)
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
                    location=location
                    if (location := lookup(row.framedipaddress)) is not None
                    else "-",
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

    def ip_to_username(self, ip_address: str) -> str | None:
        """
        in internet service we only has user ip address because they are only
        using microtik for login and etc.
        please note that ip 172.25.220.147 (openvpn)
        is use only for testing purpose so I return my username.
        """
        if ip_address == "172.25.220.147":
            return "parham.alvani"

        statement = (
            select(RadiusAccount)
            .where(RadiusAccount.framedipaddress == ip_address)
            .where(RadiusAccount.account_stop_time == None)
        )
        row = self.session.scalars(statement).first()
        if row is None:
            return None
        return row.username
