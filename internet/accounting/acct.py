"""
accouting servier source file.
this service used for accessing free-radius database
to manage account and usage.
"""
from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from internet.model.radacct import RadiusAccount
from internet.model.raddaily import RadiusDaily
from internet.model.radpackages import RadiusPackages
from internet.model.radusergroup import RadiusUserGroup
from internet.subnets import lookup
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
        statement_1 = (
            select(RadiusDaily)
            .where(RadiusDaily.username == username)
            .where(
                RadiusDaily.create_date
                > (datetime.now() + timedelta(days=-30)).date()
            )
        )
        for row_1 in self.session.scalars(statement_1):
            usage_history.append(
                UsageRecord(
                    discount=row_1.usage_original - row_1.usage_discount,
                    usage=row_1.usage_discount,
                    created_date=row_1.create_date,
                )
            )

            usage.daily += (
                row_1.usage_discount
                if row_1.create_date
                > (datetime.now() + timedelta(days=-1)).date()
                else 0
            )
            usage.weekly += (
                row_1.usage_discount
                if row_1.create_date
                > (datetime.now() + timedelta(days=-7)).date()
                else 0
            )
            usage.monthly += row_1.usage_discount

        usage.free = usage.monthly
        usage_history.reverse()

        # sessions from radius account table
        sessions: list[IESession] = []
        statement_2 = (
            select(RadiusAccount)
            .where(RadiusAccount.username == username)
            .where(RadiusAccount.account_stop_time == None)
        )
        for row_2 in self.session.scalars(statement_2):
            sessions.append(
                IESession(
                    ip=row_2.framedipaddress,
                    id=row_2.account_unique_id,
                    time=row_2.account_start_time,
                    usage=row_2.account_input_octets
                    + row_2.account_output_octets,
                    # location information must calculate
                    # based on ip address.
                    location=location
                    if (location := lookup(row_2.framedipaddress)) is not None
                    else "-",
                    is_current=False,
                )
            )

        # user's groupname
        group_name = ""
        package: Package = Package()
        statement_3 = select(RadiusUserGroup).where(
            RadiusUserGroup.username == username
        )
        row_3 = self.session.scalars(statement_3).first()
        if row_3 is not None:
            group_name = row_3.group_name
            # gather packages for the group
            statement_4 = select(RadiusPackages).where(
                RadiusPackages.group_name
                == group_name.split("-", maxsplit=1)[0]
            )
            row_4 = self.session.scalars(statement_4).first()
            if row_4 is not None:
                package = Package(
                    daily_volume=row_4.daily_volume,
                    weekly_volume=row_4.weekly_volume,
                    monthly_volume=row_4.monthly_volume,
                    free_volume=4 * row_4.monthly_volume,
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
