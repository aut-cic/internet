import typing

import sanic
from sanic.log import logger
from sanic.response import redirect
from sanic_ext import render


class StatusHandler:
    @staticmethod
    async def status(request: sanic.Request) -> sanic.HTTPResponse:
        app = typing.cast(sanic.Sanic, request.app)

        ip = request.ip
        logger.info(f"request from {ip}")
        if ip.startswith(("192", "172")) is False:
            return redirect(app.url_for("site.login"))

        return await render(
            "status.html",
            context={},
            status=200,
        )

    def register(self) -> sanic.Blueprint:
        bp = sanic.Blueprint("status", url_prefix="/")
        bp.add_route(self.status, "/status", methods=["GET"], name="status")

        return bp
