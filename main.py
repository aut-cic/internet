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

    pretty.pprint(list(internet.subnets.list()))

    pretty.pprint(list(internet.announcements.list()))

    engine = create_engine(
        f"mysql+pymysql://{cfg.database.username}:{cfg.database.password}@{cfg.database.host}:{cfg.database.port}/{cfg.database.database}",
        echo=False,
        future=True,
    )

    app = internet.http.main.app(cfg.login_url, cfg.logout_url, engine)
    app.run(host="0.0.0.0", port=8080, debug=False)
