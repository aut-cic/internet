import logging

import sanic

from .site import SiteHandler


def app(login_url: str) -> sanic.Sanic:
    app = sanic.Sanic("internet")
    # logger in the context which is useful for handlers
    app.ctx.logger = logging.getLogger("internet.http")
    app.ctx.login_url = login_url

    app.blueprint(SiteHandler().register())

    app.static("/static", "./frontend/dist", name="static")
    app.static("/public", "./public", name="public")

    return app
