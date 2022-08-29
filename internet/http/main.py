import sanic
from sanic.exceptions import NotFound
from sqlalchemy.future import Engine

from internet.http.site.view import index, bp as site_bp
from internet.http.status.view import bp as status_bp


def create_app(login_url: str, logout_url: str, engine: Engine) -> sanic.Sanic:
    """
    create sanic application and inject dependencies into context
    """
    app = sanic.Sanic("internet")
    app.ctx.login_url = login_url
    app.ctx.logout_url = logout_url
    app.ctx.engine = engine

    # configuration for using internet service behind nginx
    app.config.PROXIES_COUNT = 1
    app.config.REAL_IP_HEADER = "x-real-ip"

    app.blueprint(site_bp)
    app.blueprint(status_bp)

    app.error_handler.add(NotFound, index)

    app.static("/static", "./frontend/dist", name="static")
    app.static("/public", "./public", name="public")

    return app
