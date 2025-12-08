"""
Login and logout routes. Login route returns a page
that sends request into free-radius server and logout
a route without any html/css.
"""

import logging
import time
from typing import Annotated

import httpx
from fastapi import APIRouter, Query, Request
from fastapi.responses import RedirectResponse

from internet.accounting.acct import AccountingService
from internet.http.dependencies import ClientIPDep, DBSessionDep, URLsDep, templates
from internet.message.message import LANGS, MESSAGES
from internet.metrics import REQUEST_COUNTER, REQUEST_LATENCY

logger = logging.getLogger(__name__)

router = APIRouter(tags=["site"])


@router.get("/logout/{sid}", name="logout")
async def logout(
    request: Request,
    sid: str,
    urls: URLsDep,
    site: Annotated[str, Query()] = "1",
) -> RedirectResponse:
    """
    Logout with sending a request into free-radius.
    """
    logger.info("logout request for %s", sid)

    start = time.time()

    logout_url = urls.logout_urls[site]

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

    REQUEST_COUNTER.labels("site", "logout").inc()
    REQUEST_LATENCY.labels("site", "logout").observe(time.time() - start)

    return RedirectResponse(url=request.url_for("login", path=""), status_code=302)


@router.api_route(
    "/{path:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"],
    name="login",
)
async def index(
    request: Request,
    session: DBSessionDep,
    urls: URLsDep,
    user_ip: ClientIPDep,
    path: str = "",
    dst: Annotated[str, Query()] = "",
    error: Annotated[str, Query()] = "",
    lang: Annotated[str, Query()] = "fa",
    site: Annotated[str, Query()] = "1",
):
    """
    Login page that must be shown on every request.
    Because we need to show login page for all not found routes.
    Mikrotik sends all requests from not logged-in users to us like follows:

    GET http://localhost:8080/d/msdownload/update/software/defu/2022/07/
    am_delta_patch_1.371.578.0_f39d3c3b511eefc28a41de387e41647c47e7aa42.exe

    and devices like iOS need to get 200 response.
    """
    start = time.time()

    logger.info("login request from %s (path: %s)", user_ip, path)

    if lang not in LANGS:
        lang = "fa"

    usage = AccountingService(session)
    if usage.ip_to_username(user_ip) is not None:
        REQUEST_COUNTER.labels("site", "login").inc()
        REQUEST_LATENCY.labels("site", "login").observe(time.time() - start)

        return RedirectResponse(url=request.url_for("status"), status_code=302)

    REQUEST_COUNTER.labels("site", "login").inc()
    REQUEST_LATENCY.labels("site", "login").observe(time.time() - start)

    login_url = urls.login_urls[site]

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "messages": {key: val[lang] for (key, val) in MESSAGES.items()},
            "error": error,
            "login_url": login_url,
            "dst": dst,
        },
        status_code=200,
    )
