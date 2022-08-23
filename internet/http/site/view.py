"""
login and logout routes. login route returns a page
that sends request into free-radius server and logout
a route without any html/css.
"""
import typing

import requests
import sanic
import sqlalchemy.future
from sanic.log import logger
from sanic.response import redirect
from sanic_ext import render
from sqlalchemy.orm import Session

from internet.accounting.acct import AccountingService
from internet.message.message import MESSAGES, LANGS


bp = sanic.Blueprint("site", url_prefix="/")


# pyre-ignore[56]
@bp.route("/", methods=["GET"], name="login")
async def index(request: sanic.Request) -> sanic.HTTPResponse:
    """
    login page
    """

    user_ip = request.remote_addr or request.ip

    logger.info("request from %s", user_ip)

    login_url = typing.cast(str, request.app.ctx.login_url)
    engine = typing.cast(sqlalchemy.future.Engine, request.app.ctx.engine)
    dst: str = request.args.get("dst", "")
    error: str = request.args.get("error", "")
    lang: str = request.args.get("lang", "fa")

    if lang not in LANGS:
        lang = "fa"

    with Session(engine) as session:
        usage = AccountingService(session)
        username = usage.ip_to_username(user_ip)
        if username is not None:
            return redirect(request.url_for("status.status"))

    return await render(
        "index.html",
        context={
            "messages": {key: val[lang] for (key, val) in MESSAGES.items()},
            "error": error,
            "login_url": login_url,
            "dst": dst,
        },
        status=200,
    )


# pyre-ignore[56]
@bp.route("/logout/<sid:str>", methods=["GET"], name="logout")
async def logout(request: sanic.Request, sid: str) -> sanic.HTTPResponse:
    """
    logout with sending a request into free-radius
    """
    logout_url = typing.cast(str, request.app.ctx.logout_url)
    logger.info("logout request for %s", sid)

    response = requests.get(f"{logout_url}/{sid}")
    if not response:
        logger.error("logout request for %s failed", sid)

    return redirect(request.url_for("site.login"))
