import sanic
from sqlalchemy.future import Engine

from .site import SiteHandler
from .status import StatusHandler


def app(
    login_url: str, logout_url: str, behind_proxy: bool, engine: Engine
) -> sanic.Sanic:
    app = sanic.Sanic("internet")
    app.ctx.login_url = login_url
    app.ctx.logout_url = logout_url
    app.ctx.engine = engine

    if behind_proxy is True:
        # configuration for using internet service behind nginx
        app.config.PROXIES_COUNT = 1
        app.config.REAL_IP_HEADER = "x-real-ip"

    app.blueprint(SiteHandler().register())
    app.blueprint(StatusHandler().register())

    app.static("/static", "./frontend/dist", name="static")
    app.static("/public", "./public", name="public")

    return app
