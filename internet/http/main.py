import sanic
from sqlalchemy.engine import Engine

from internet.http.site.view import bp as site_bp
from internet.http.status.view import bp as status_bp
from internet.model.urls import URLs


def create_app(login_url: str, logout_url: str, engine: Engine) -> sanic.Sanic:
    """
    create sanic application and inject dependencies into context
    """
    app = sanic.Sanic("internet")
    app.ext.dependency(engine)
    app.ext.dependency(URLs(login_url, logout_url))

    # configuration for using internet service behind nginx
    app.config.PROXIES_COUNT = 1
    app.config.REAL_IP_HEADER = "x-real-ip"

    app.blueprint(site_bp)
    app.blueprint(status_bp)

    app.static(
        "/static", "./frontend/dist", name="static", stream_large_files=True
    )
    app.static("/public", "./public", name="public")

    return app
