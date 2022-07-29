import typing

import sanic
import sqlalchemy.future
from sanic.log import logger
from sanic.response import redirect
from sanic_ext import render
from sqlalchemy.orm import Session

from ..accounting.acct import AccountingService


class StatusHandler:
    @staticmethod
    async def status(request: sanic.Request) -> sanic.HTTPResponse:
        app = typing.cast(sanic.Sanic, request.app)
        engine = typing.cast(sqlalchemy.future.Engine, request.app.ctx.engine)

        ip = request.ip
        logger.info(f"request from {ip}")

        if ip.startswith(("192", "172")) is False:
            return redirect(app.url_for("site.login"))

        with Session(engine) as session:
            usage = AccountingService(session)
            username = usage.ip_to_username(ip)
            if username is None:
                return redirect(app.url_for("site.login"))

            report = usage.user_usage(username)

            return await render(
                "status.html",
                context={},
                status=200,
            )

    def register(self) -> sanic.Blueprint:
        bp = sanic.Blueprint("status", url_prefix="/")
        bp.add_route(self.status, "/status", methods=["GET"], name="status")

        return bp
