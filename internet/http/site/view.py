"""
login and logout routes. login route returns a page
that sends request into free-radius server and logout
a route without any html/css.
"""
import time

import httpx
import sanic
import sqlalchemy.future
from sqlalchemy.orm import Session
from sanic.log import logger
from sanic.response import redirect
from sanic_ext import render

from internet.accounting.acct import AccountingService
from internet.message.message import MESSAGES, LANGS
from internet.metrics import REQUEST_COUNTER, REQUEST_LATENCY
from internet.model.urls import URLs


bp = sanic.Blueprint("site", url_prefix="/")


# pyre-ignore[56]
@bp.route("/logout/<sid:str>", methods=["GET"], name="logout")
async def logout(
    request: sanic.Request, sid: str, urls: URLs
) -> sanic.HTTPResponse:
    """
    logout with sending a request into free-radius
    """
    logger.info("logout request for %s", sid)

    start = time.time()

    try:
        async with httpx.AsyncClient() as client:
            if not await client.get(f"{urls.logout_url}/{sid}"):
                logger.error("logout request for %s failed", sid)
    except (httpx.ConnectTimeout, httpx.ConnectError) as exception:
        logger.error("logout request for %s failed (%s)", sid, repr(exception))
    except (httpx.ReadTimeout, httpx.ReadError) as exception:
        logger.error(
            "logout request success but there is an issue for reading %s (%s)",
            sid,
            repr(exception),
        )

    REQUEST_COUNTER.labels("site", "logout").inc()
    REQUEST_LATENCY.labels("site", "logout").observe(time.time() - start)

    return redirect(request.url_for("site.login"))


# pyre-ignore[56]
@bp.route("/<path:path>", methods=["GET", "POST"], name="login")
async def index(
    request: sanic.Request,
    engine: sqlalchemy.engine.Engine,
    urls: URLs,
    path: str = "",
) -> sanic.HTTPResponse:
    """
    login page that must be shown on every requests.
    because we need to show login page for all not found routes.
    Mircotik sends
    all requests from not logged-in users to us like follows:

    GET http://localhost:8080/d/msdownload/update/software/defu/2022/07/
    am_delta_patch_1.371.578.0_f39d3c3b511eefc28a41de387e41647c47e7aa42.exe

    and devices like ios needs to get 200 response.
    """
    start = time.time()
    user_ip = request.remote_addr or request.ip

    logger.info("login request from %s (path: %s)", user_ip, path)

    dst: str = request.args.get("dst", "")
    error: str = request.args.get("error", "")

    if (lang := request.args.get("lang", "fa")) not in LANGS:
        lang = "fa"

    with Session(engine) as session:
        usage = AccountingService(session)
        if usage.ip_to_username(user_ip) is not None:
            REQUEST_COUNTER.labels("site", "login").inc()
            REQUEST_LATENCY.labels("site", "login").observe(
                time.time() - start
            )

            return redirect(request.url_for("status.status"))

    REQUEST_COUNTER.labels("site", "login").inc()
    REQUEST_LATENCY.labels("site", "login").observe(time.time() - start)

    return await render(
        "index.html",
        context={
            "messages": {key: val[lang] for (key, val) in MESSAGES.items()},
            "error": error,
            "login_url": urls.login_url,
            "dst": dst,
        },
        status=200,
    )
