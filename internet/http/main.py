import sanic
from sanic.response import redirect
from sanic.exceptions import NotFound
from sqlalchemy.future import Engine
from sanic.log import logger

from .site import SiteHandler
from .status import StatusHandler


async def not_found_handler(request: sanic.Request, _):
    """
    redirect all not found routes to login page. Mircotik sends
    all requests from not logged-in users to us like follows:

    GET http://localhost:8080/d/msdownload/update/software/defu/2022/07/
    am_delta_patch_1.371.578.0_f39d3c3b511eefc28a41de387e41647c47e7aa42.exe
    """
    logger.info("redirect from %s", request.path)

    return redirect(request.app.url_for("site.login"))


def create_app(login_url: str, logout_url: str, engine: Engine) -> sanic.Sanic:
    """
    create sanic application and inject dependencies into context
    """
    app = sanic.Sanic("internet")
    app.ctx.login_url = login_url
    app.ctx.logout_url = logout_url
    app.ctx.engine = engine

    app.error_handler.add(NotFound, not_found_handler)

    # configuration for using internet service behind nginx
    app.config.PROXIES_COUNT = 1
    app.config.REAL_IP_HEADER = "x-real-ip"

    app.blueprint(SiteHandler().register())
    app.blueprint(StatusHandler().register())

    app.static("/static", "./frontend/dist", name="static")
    app.static("/public", "./public", name="public")

    return app
