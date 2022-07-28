import logging

import sanic

from .site import SiteHandler
from .status import StatusHandler


def app(login_url: str) -> sanic.Sanic:
    app = sanic.Sanic("internet")
    app.ctx.login_url = login_url

    app.blueprint(SiteHandler().register())
    app.blueprint(StatusHandler().register())

    app.static("/static", "./frontend/dist", name="static")
    app.static("/public", "./public", name="public")

    return app
