import typing

import sanic
from sanic.log import logger
from sanic.response import redirect


class SiteHandler:
    @staticmethod
    async def logout(request: sanic.Request, sid: str) -> sanic.HTTPResponse:
        app = typing.cast(sanic.Sanic, request.app)
        logger.info(f"logout request for {sid}")
        return redirect(app.url_for("site.login"))

    def register(self) -> sanic.Blueprint:
        bp = sanic.Blueprint("logout", url_prefix="/")
        bp.add_route(
            self.logout, "/logout/<sid:str>", methods=["GET"], name="login"
        )

        return bp
