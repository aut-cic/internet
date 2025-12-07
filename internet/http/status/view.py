import math
import random
import time
import typing

import jdatetime
import sanic
import sqlalchemy.future
from sanic.log import logger
from sanic.response import redirect
from sanic_ext import render
from sqlalchemy.orm import Session

from internet.accounting.acct import AccountingService
from internet.accounting.usage import Report, UsageRecord, UsageType, bytes_to_str
from internet.accounting.usage import Session as IESession
from internet.announcements import announcements
from internet.metrics import REQUEST_COUNTER, REQUEST_LATENCY

jdatetime.set_locale("fa_IR")

bp = sanic.Blueprint("status", url_prefix="/")

danger_packages: set[UsageType] = {UsageType.MONTHLY, UsageType.FREE}

titles: dict[UsageType, str] = {
    UsageType.DAILY: "امروز",
    UsageType.WEEKLY: "7 روز اخیر",
    UsageType.MONTHLY: "30 روز اخیر",
    UsageType.FREE: "آزاد",
}

colors: dict[UsageType, str] = {
    UsageType.DAILY: "success",
    UsageType.WEEKLY: "primary",
    UsageType.MONTHLY: "info",
    UsageType.FREE: "warning",
}

speeds: dict[UsageType, str] = {
    UsageType.DAILY: "سرعت نامحدود",
    UsageType.WEEKLY: "سرعت زیاد",
    UsageType.MONTHLY: "سرعت 2M",
    UsageType.FREE: "سرعت کم",
}


def to_frontend_usage_history(
    usage_history: list[UsageRecord],
) -> list[typing.Any]:
    """
    covert usage history from report into frontend usage history
    which contains the required information for status html page.
    """
    result = []
    for record in sorted(
        usage_history,
        key=lambda record: record.created_date,
    ):
        result.append(
            {
                "date": jdatetime.date.fromgregorian(
                    date=record.created_date,
                ).strftime("%d/%m/%Y"),
                "usage": record.usage,
                "discount": record.discount,
            }
        )
    return result


def to_frontend_session(session: IESession, current_ip: str) -> typing.Any:
    """
    covert session from report into a frontend session which contains
    the required information for status html page.
    """
    session.is_current = session.ip == current_ip

    return {
        "ip": session.ip,
        "time": jdatetime.datetime.fromgregorian(
            datetime=session.time,
        ).strftime("%H:%M:%S - %d/%m/%Y"),
        "usage": "-" if session.usage < 1000 else bytes_to_str(session.usage),
        "id": session.id,
        "location": session.location,
        "is_current": session.is_current,
    }


def to_frontend_package(report: Report, usage_type: UsageType) -> typing.Any:
    """
    create package description which is useful for status html package.
    please note that package volumes in GB so we need to convert them into
    byte.
    again meaning of these data is only valid on html/css so please check
    them there.
    """
    percent: float = 0.0
    usage: str = ""
    usage_number: int = 0
    total: str = ""
    try:
        match usage_type:
            case UsageType.DAILY:
                percent = (
                    report.usage.daily
                    / (report.package.daily_volume * (1024**3))
                ) * 100
                usage = bytes_to_str(report.usage.daily, "en")
                usage_number = report.usage.daily
                total = bytes_to_str(
                    report.package.daily_volume * (1024**3),
                    "en",
                )
            case UsageType.WEEKLY:
                percent = (
                    report.usage.weekly
                    / (report.package.weekly_volume * (1024**3))
                ) * 100
                usage = bytes_to_str(report.usage.weekly, "en")
                usage_number = report.usage.weekly
                total = bytes_to_str(
                    report.package.weekly_volume * (1024**3), "en"
                )
            case UsageType.MONTHLY:
                percent = (
                    report.usage.monthly
                    / (report.package.monthly_volume * (1024**3))
                ) * 100
                usage = bytes_to_str(report.usage.monthly, "en")
                usage_number = report.usage.monthly
                total = bytes_to_str(
                    report.package.monthly_volume * (1024**3), "en"
                )
            case UsageType.FREE:
                percent = (
                    report.usage.free
                    / (report.package.free_volume * (1024**3))
                ) * 100
                usage = bytes_to_str(report.usage.free, "en")
                usage_number = report.usage.free
                total = bytes_to_str(
                    report.package.free_volume * (1024**3), "en"
                )
    except ZeroDivisionError:
        percent = 100

    percent = min(percent, 100)

    color = "success"
    if percent > 66:
        color = "danger"
    elif percent > 33:
        color = "warning"

    return {
        "usage": usage,
        "usageNum": usage_number,
        "total": total,
        "percent": percent,
        "degree": math.floor(percent / (100.0 / 180)),
        "title": titles[usage_type],
        "speed": speeds[usage_type],
        "color": color,
        "cardColor": colors[usage_type],
        "type": str(usage_type),
        "active": usage_type is report.get_active_type(),
        "danger": usage_type in danger_packages,
    }


# pyre-ignore[56]
@bp.route("/status", methods=["GET"], name="status")
async def status(
    request: sanic.Request, engine: sqlalchemy.engine.Engine
) -> sanic.HTTPResponse:
    """
    status gather all the information into a frontend-compatible
    way to serve /status page.
    """
    start = time.time()

    user_ip = request.remote_addr or request.ip

    logger.info("status request from %s", user_ip)

    # please note that "127.0.0.*" is only for testing purposes.
    # other domains are the valid aut domains.
    if not user_ip.startswith(("192", "172", "127.0.0")):
        return redirect(request.url_for("site.login", path=""))

    with Session(engine) as session:
        usage = AccountingService(session)
        if (username := usage.ip_to_username(user_ip)) is None:
            logger.info("there is no login session with %s", user_ip)
            return redirect(request.url_for("site.login", path=""))

        logger.info("status request from %s with %s", username, user_ip)

        report = usage.user_usage(username)

        packages = []
        # calculate usage per package (daily, weekly, monthly and free)
        for usage_type in UsageType:
            packages.append(to_frontend_package(report, usage_type))

        sessions = []
        current_session = None
        for ie_session in report.sessions:
            sessions.append(to_frontend_session(ie_session, user_ip))
            if ie_session.is_current is True:
                current_session = sessions[-1]

        usage_history = to_frontend_usage_history(report.usage_history)

        history: typing.Any = {"labels": [], "discount": [], "usage": []}
        for record in usage_history:
            history["labels"].append(record["date"])
            history["discount"].append(record["discount"])
            history["usage"].append(record["usage"])

        REQUEST_COUNTER.labels("status", "status").inc()
        REQUEST_LATENCY.labels("status", "status").observe(time.time() - start)

        return await render(
            "status.html",
            context={
                "username": report.username,
                "group": report.groupname.split("-", maxsplit=1)[0],
                "ip": user_ip,
                "location": current_session["location"]
                if current_session is not None
                else "-",
                "announcements": [
                    annc for annc in announcements() if annc.status is True
                ],
                "rand": math.floor(random.random() * 1000),
                "auth": False,
                "dst": "",
                "logout": "",
                "status": {
                    "packages": packages,
                    "group": report.groupname.split("-", maxsplit=1)[0],
                    "username": report.username,
                    "active_type": str(report.get_active_type()),
                    "sessions": sessions,
                    "current_session": current_session,
                    "usageHistory": usage_history,
                },
                "history": history,
            },
            status=200,
        )
