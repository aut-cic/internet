"""
runs internet server
"""

from rich import pretty
from sqlalchemy import create_engine
from prometheus_client import start_http_server

import internet.conf
import internet.http.main
import internet.subnets
import internet.announcements


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
    pool_size=5,
    pool_pre_ping=True,
)

app = internet.http.main.create_app(cfg.login_url, cfg.logout_url, engine)

if __name__ == "__main__":
    # start the Prometheus metrics server
    start_http_server(1373)

    app.run(
        host=cfg.listen.host,
        port=cfg.listen.port,
        debug=False,
        fast=cfg.listen.fast,
        workers=cfg.listen.workers,
        access_log=False,
    )
