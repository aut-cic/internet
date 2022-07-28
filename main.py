"""
runs internet server
"""

from rich import pretty
from rich.console import Console

import internet.conf
import internet.http.main

if __name__ == "__main__":
    console = Console()
    pretty.install()

    cfg = internet.conf.load()
    pretty.pprint(cfg)

    app = internet.http.main.app(cfg.login_url)
    app.run(host="0.0.0.0", port=8080, debug=False)
