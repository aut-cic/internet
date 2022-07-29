"""
hands-on module is useful for testing on the production
machine. set environment manually and this script will test
database connection etc. for you.
"""

from rich import pretty
from rich.console import Console
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from internet.accounting.acct import AccountingService


def account_usage():
    """
    for hands-on testing on production environment with radius database.
    replace engine url with the production url before any testing.
    """
    engine = create_engine(
        "mysql+pymysql://root:root@127.0.0.1/db",
        echo=True,
        future=True,
    )

    with Session(engine) as session:
        usage = AccountingService(session)
        res = usage.user_usage("parham.alvani")
        pretty.pprint(res)


if __name__ == "__main__":
    console = Console()
    pretty.install()

    account_usage()
