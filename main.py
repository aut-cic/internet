"""
runs internet server
"""

from rich import pretty
from rich.console import Console
from sqlalchemy import create_engine

import internet.conf
import internet.http.main
import internet.subnets
import internet.announcements

if __name__ == "__main__":
    console = Console()
    pretty.install()

    cfg = internet.conf.load()
    pretty.pprint(cfg)

    pretty.pprint(list(internet.subnets.subnets()))

    pretty.pprint(list(internet.announcements.announcements()))

    engine = create_engine(
        f"mysql+pymysql://{cfg.database.username}:{cfg.database.password}@"
        f"{cfg.database.host}:{cfg.database.port}/{cfg.database.database}",
        echo=False,
        future=True,
        pool_pre_ping=True,
    )

    app = internet.http.main.create_app(cfg.login_url, cfg.logout_url, engine)
    app.run(
        host=cfg.listen.host,
        port=cfg.listen.port,
        debug=False,
        fast=cfg.listen.fast,
        workers=cfg.listen.workers,
    )
