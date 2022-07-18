import logging

import sanic

from .site import SiteHandler


def app() -> sanic.Sanic:
    app = sanic.Sanic('internet')
    app.ctx.logger = logging.getLogger('internet.http')

    app.blueprint(SiteHandler().register())

    return app
