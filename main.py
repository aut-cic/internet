"""
runs internet server
"""

import os

import prometheus_client
import prometheus_client.multiprocess
from rich import pretty
from sanic import raw
from sqlalchemy import create_engine

import internet.announcements
import internet.conf
import internet.http.main
import internet.subnets

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

app = internet.http.main.create_app(cfg.login_urls, cfg.logout_urls, engine)

os.environ["PROMETHEUS_MULTIPROC_DIR"] = "./prom"


@app.route("/metrics", methods=["GET"])
async def expose_metrics(_):
    registry = prometheus_client.CollectorRegistry()
    prometheus_client.multiprocess.MultiProcessCollector(registry)
    data = prometheus_client.generate_latest(registry)
    return raw(data, content_type=prometheus_client.CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    # start the Prometheus metrics server
    app.run(
        host=cfg.listen.host,
        port=cfg.listen.port,
        debug=False,
        fast=cfg.listen.fast,
        workers=cfg.listen.workers,
        access_log=False,
    )
