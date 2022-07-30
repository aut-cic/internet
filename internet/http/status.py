import math
import random
import typing

import jdatetime
import sanic
import sqlalchemy.future
from sanic.log import logger
from sanic.response import redirect
from sanic_ext import render
from sqlalchemy.orm import Session

from ..accounting.acct import AccountingService
from ..accounting.usage import Report
from ..accounting.usage import Session as IESession
from ..accounting.usage import UsageRecord, UsageType, bytes_to_str

jdatetime.set_locale("fa_IR")


class StatusHandler:
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

    @staticmethod
    def to_frontend_usage_history(
        usage_history: list[UsageRecord],
    ) -> list[typing.Any]:
        """
        covert usage history from report into frontend usage history
        which contains the required information for status html page.
        """
        result = []
        for record in usage_history:
            result.append(
                {
                    "date": jdatetime.date.fromgregorian(
                        date=record.created_date,
                    ).strftime("%d/%m/%Y"),
                    "usageHuman": bytes_to_str(record.usage),
                    "usage": record.usage,
                    "discountHuman": bytes_to_str(record.discount),
                    "discount": record.discount,
                }
            )
        result.sort(key=lambda record: record["date"], reverse=True)
        return result

    @staticmethod
    def to_frontend_session(session: IESession, ip: str) -> typing.Any:
        """
        covert session from report into a frontend session which contains
        the required information for status html page.
        """
        session.is_current = session.ip == ip

        return {
            "ip": session.ip,
            "time": jdatetime.datetime.fromgregorian(
                datetime=session.time,
            ).strftime("%H:%M:%S - %d/%m/%Y"),
            "usage": "-"
            if session.usage < 1000
            else bytes_to_str(session.usage),
            "id": session.id,
            "location": session.location,
            "is_current": session.is_current,
        }

    @staticmethod
    def to_frontend_package(report: Report, type: UsageType) -> typing.Any:
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
            match type:
                case UsageType.DAILY:
                    percent = (
                        report.usage.daily
                        / (report.package.daily_volume * (1024**3))
                    ) * 100
                    usage = bytes_to_str(report.usage.daily)
                    usage_number = report.usage.daily
                    total = bytes_to_str(
                        report.package.daily_volume * (1024**3)
                    )
                case UsageType.WEEKLY:
                    percent = (
                        report.usage.weekly
                        / (report.package.weekly_volume * (1024**3))
                    ) * 100
                    usage = bytes_to_str(report.usage.weekly)
                    usage_number = report.usage.weekly
                    total = bytes_to_str(
                        report.package.weekly_volume * (1024**3)
                    )
                case UsageType.MONTHLY:
                    percent = (
                        report.usage.monthly
                        / (report.package.monthly_volume * (1024**3))
                    ) * 100
                    usage = bytes_to_str(report.usage.monthly)
                    usage_number = report.usage.monthly
                    total = bytes_to_str(
                        report.package.monthly_volume * (1024**3)
                    )
                case UsageType.FREE:
                    percent = (
                        report.usage.free
                        / (report.package.free_volume * (1024**3))
                    ) * 100
                    usage = bytes_to_str(report.usage.free)
                    usage_number = report.usage.free
                    total = bytes_to_str(
                        report.package.free_volume * (1024**3)
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
            "title": StatusHandler.titles[type],
            "title2": StatusHandler.speeds[type],
            "color": color,
            "color2": StatusHandler.colors[type],
            "type": str(type),
            "active": type is report.get_active_type(),
        }

    @staticmethod
    async def status(request: sanic.Request) -> sanic.HTTPResponse:
        app = typing.cast(sanic.Sanic, request.app)
        engine = typing.cast(sqlalchemy.future.Engine, request.app.ctx.engine)

        ip = request.ip
        logger.info(f"request from {ip}")

        # please note that "127.0.0.*" is only for testing purposes.
        if ip.startswith(("192", "172", "127.0.0")) is False:
            return redirect(app.url_for("site.login"))

        with Session(engine) as session:
            usage = AccountingService(session)
            username = usage.ip_to_username(ip)
            if username is None:
                logger.info(f"there is no login session with {ip}")
                return redirect(app.url_for("site.login"))

            report = usage.user_usage(username)

            packages = []
            # calculate usage per package (daily, weekly, monthly and free)
            for usage_type in UsageType:
                packages.append(
                    StatusHandler.to_frontend_package(report, usage_type)
                )

            sessions = []
            current_session = None
            for ie_session in report.sessions:
                sessions.append(
                    StatusHandler.to_frontend_session(ie_session, ip)
                )
                if ie_session.is_current is True:
                    current_session = sessions[-1]

            usage_history = StatusHandler.to_frontend_usage_history(
                report.usage_history
            )

            history: typing.Any = {"labels": [], "discount": [], "usage": []}
            for record in usage_history:
                history["labels"].append(record["date"])
                history["discount"].append(record["discount"])
                history["usage"].append(record["usage"])

            return await render(
                "status.html",
                context={
                    "username": report.username,
                    "group": report.groupname.split("-", maxsplit=1)[0],
                    "ip": request.ip,
                    "location": current_session["location"]
                    if current_session is not None
                    else "-",
                    "announcements": [],
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

    def register(self) -> sanic.Blueprint:
        bp = sanic.Blueprint("status", url_prefix="/")
        bp.add_route(self.status, "/status", methods=["GET"], name="status")

        return bp
