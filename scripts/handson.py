"""
hands-on module is useful for testing on the production
machine. set environment manually and this script will test
database connection etc. for you.
"""

from rich import pretty
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from internet.accounting.acct import AccountingService
from internet.accounting.usage import Report, UsageType
from internet.http.status.view import to_frontend_package, to_frontend_session


def ip_to_username_with_taheri() -> None:
    """
    convert mr.taheri machine ip address into username
    """
    engine = create_engine(
        "mysql+pymysql://root:root@127.0.0.1/db",
        echo=True,
        future=True,
    )

    with Session(engine) as session:
        usage = AccountingService(session)
        username = usage.ip_to_username("172.25.22.10")
        pretty.pprint(username)


def account_usage() -> None:
    """
    for hands-on testing on production environment with radius database.
    replace engine url with the production url before any testing.
    """
    engine = create_engine(
        "mysql+pymysql://root:root@127.0.0.1/db",
        echo=True,
        future=True,
    )

    report: Report
    with Session(engine) as session:
        usage = AccountingService(session)
        report = usage.user_usage("parham.alvani")
        pretty.pprint(report)

    for usage_type in UsageType:
        pretty.pprint(to_frontend_package(report, usage_type))

    for internet_session in report.sessions:
        pretty.pprint(to_frontend_session(internet_session, "172.25.125.2"))


if __name__ == "__main__":
    pretty.install()

    ip_to_username_with_taheri()
    account_usage()
