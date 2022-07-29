import typing

import sanic
from sanic.log import logger
from sanic.response import redirect
from sanic_ext import render

from ..message.message import MESSAGES


class SiteHandler:
    @staticmethod
    async def index(request: sanic.Request) -> sanic.HTTPResponse:
        login_url = typing.cast(str, request.app.ctx.login_url)
        dst = request.get_args().get("dst", "")

        return await render(
            "index.html",
            context={
                "messages": MESSAGES,
                "login_url": login_url,
                "dst": dst,
            },
            status=200,
        )

    @staticmethod
    async def logout(request: sanic.Request, sid: str) -> sanic.HTTPResponse:
        app = typing.cast(sanic.Sanic, request.app)
        logger.info(f"logout request for {sid}")
        return redirect(app.url_for("site.login"))

    def register(self) -> sanic.Blueprint:
        bp = sanic.Blueprint("site", url_prefix="/")
        bp.add_route(self.index, "/", methods=["GET"], name="login")
        bp.add_route(
            self.logout, "/logout/<sid:str>", methods=["GET"], name="logout"
        )

        return bp
