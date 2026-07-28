"""
Runs internet server.
"""

from sqlalchemy import create_engine

import internet.conf
import internet.http.main
from internet.model.urls import URLs

cfg = internet.conf.load()

engine = create_engine(
    f"mysql+pymysql://{cfg.database.username}:{cfg.database.password}@"
    f"{cfg.database.host}:{cfg.database.port}/{cfg.database.database}",
    echo=False,
    pool_size=5,
    pool_pre_ping=True,
)

app = internet.http.main.create_app(URLs(cfg.login_urls, cfg.logout_urls), engine)


if __name__ == "__main__":
    import uvicorn
    from rich import pretty

    pretty.install()
    pretty.pprint(cfg)

    uvicorn.run(
        "main:app",
        host=cfg.listen.host,
        port=cfg.listen.port,
        workers=cfg.listen.workers,
        log_level="info",
        proxy_headers=True,
        forwarded_allow_ips="*",
        access_log=True,
    )
