"""
login and logout routes. login route returns a page
that sends request into free-radius server and logout
a route without any html/css.
"""
import typing

import httpx
import sanic
import sqlalchemy.future
from sqlalchemy.orm import Session
from sanic.log import logger
from sanic.response import redirect
from sanic_ext import render

from internet.accounting.acct import AccountingService
from internet.message.message import MESSAGES, LANGS


bp = sanic.Blueprint("site", url_prefix="/")


# pyre-ignore[56]
@bp.route("/", methods=["GET"], name="login")
async def index(request: sanic.Request, _=None) -> sanic.HTTPResponse:
    """
    login page that must be shown on every requests.
    because we need to show login page for all not found routes.
    Mircotik sends
    all requests from not logged-in users to us like follows:

    GET http://localhost:8080/d/msdownload/update/software/defu/2022/07/
    am_delta_patch_1.371.578.0_f39d3c3b511eefc28a41de387e41647c47e7aa42.exe

    and devices like ios needs to get 200 response.
    """
    user_ip = request.remote_addr or request.ip

    logger.info("login request from %s", user_ip)

    login_url = typing.cast(str, request.app.ctx.login_url)
    engine = typing.cast(sqlalchemy.future.Engine, request.app.ctx.engine)
    dst: str = request.args.get("dst", "")
    error: str = request.args.get("error", "")

    if (lang := request.args.get("lang", "fa")) not in LANGS:
        lang = "fa"

    with Session(engine) as session:
        usage = AccountingService(session)
        if usage.ip_to_username(user_ip) is not None:
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

    try:
        async with httpx.AsyncClient() as client:
            if not await client.get(f"{logout_url}/{sid}"):
                logger.error("logout request for %s failed", sid)
    except (httpx.ConnectTimeout, httpx.ConnectError) as exception:
        logger.error("logout request for %s failed (%s)", sid, repr(exception))
    except (httpx.ReadTimeout, httpx.ReadError) as exception:
        logger.error(
            "logout request success but there is an issue for reading %s (%s)",
            sid,
            repr(exception),
        )

    return redirect(request.url_for("site.login"))
