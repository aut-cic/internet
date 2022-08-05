import typing

import requests
import sanic
import sqlalchemy.future
from sanic.log import logger
from sanic.response import redirect
from sanic_ext import render
from sqlalchemy.orm import Session

from ..accounting.acct import AccountingService
from ..message.message import MESSAGES, LANGS


class SiteHandler:
    """
    login and logout routes. login route returns a page
    that sends request into free-radius server and logout
    a route without any html/css.
    """

    @staticmethod
    async def index(request: sanic.Request) -> sanic.HTTPResponse:
        """
        login page
        """
        login_url = typing.cast(str, request.app.ctx.login_url)
        app = typing.cast(sanic.Sanic, request.app)
        engine = typing.cast(sqlalchemy.future.Engine, request.app.ctx.engine)
        dst = request.args.get("dst", "")
        lang = request.args.get("lang", "fa")

        if lang not in LANGS:
            lang = "fa"

        with Session(engine) as session:
            usage = AccountingService(session)
            username = usage.ip_to_username(request.ip)
            if username is not None:
                return redirect(app.url_for("status.status"))

        return await render(
            "index.html",
            context={
                "messages": {key: val[lang] for (key, val) in MESSAGES.items()},
                "login_url": login_url,
                "dst": dst,
            },
            status=200,
        )

    @staticmethod
    async def logout(request: sanic.Request, sid: str) -> sanic.HTTPResponse:
        """
        logout with sending a request into free-radius
        """
        app = typing.cast(sanic.Sanic, request.app)
        logout_url = typing.cast(str, request.app.ctx.logout_url)
        logger.info(f"logout request for {sid}")

        response = requests.get(f"{logout_url}/{sid}")
        if not response:
            logger.error(f"logout request for {sid} failed")

        return redirect(app.url_for("site.login"))

    def register(self) -> sanic.Blueprint:
        """
        registers routes as a Blueprint.
        """
        bp = sanic.Blueprint("site", url_prefix="/")
        bp.add_route(self.index, "/", methods=["GET"], name="login")
        bp.add_route(self.logout, "/logout/<sid:str>", methods=["GET"], name="logout")

        return bp
