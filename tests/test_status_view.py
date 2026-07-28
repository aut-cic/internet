"""
Tests for the pure presentation helpers behind the status page.
"""

from datetime import datetime

from internet.accounting.usage import Package, Report, Usage, UsageType
from internet.accounting.usage import Session as IESession
from internet.http.status.view import to_frontend_package, to_frontend_session


def make_report(usage: Usage, package: Package, groupname: str = "students") -> Report:
    return Report(
        usage_history=[],
        package=package,
        groupname=groupname,
        usage=usage,
        username="someone",
        sessions=[],
    )


def test_to_frontend_package_computes_percentage() -> None:
    gigabyte = 1024**3
    report = make_report(Usage(daily=gigabyte), Package(daily_volume=2))

    package = to_frontend_package(report, UsageType.DAILY)

    assert package["percent"] == 50.0
    assert package["usage"] == "1 GB"
    assert package["total"] == "2 GB"


def test_to_frontend_package_clamps_overuse_to_full() -> None:
    gigabyte = 1024**3
    report = make_report(Usage(daily=10 * gigabyte), Package(daily_volume=2))

    package = to_frontend_package(report, UsageType.DAILY)

    # A gauge cannot go past 100% even when the user blew through the quota.
    assert package["percent"] == 100
    assert package["degree"] == 180


def test_to_frontend_package_treats_zero_quota_as_full() -> None:
    report = make_report(Usage(daily=1), Package(daily_volume=0))

    package = to_frontend_package(report, UsageType.DAILY)

    # Dividing by a zero-volume package must not raise.
    assert package["percent"] == 100


def test_to_frontend_package_colour_thresholds() -> None:
    gigabyte = 1024**3
    quota = Package(daily_volume=100)

    low = to_frontend_package(
        make_report(Usage(daily=10 * gigabyte), quota), UsageType.DAILY
    )
    mid = to_frontend_package(
        make_report(Usage(daily=50 * gigabyte), quota), UsageType.DAILY
    )
    high = to_frontend_package(
        make_report(Usage(daily=90 * gigabyte), quota), UsageType.DAILY
    )

    assert low["color"] == "success"
    assert mid["color"] == "warning"
    assert high["color"] == "danger"


def test_to_frontend_package_marks_the_active_tier() -> None:
    report = make_report(Usage(), Package(), groupname="students-H2")

    monthly = to_frontend_package(report, UsageType.MONTHLY)
    daily = to_frontend_package(report, UsageType.DAILY)

    assert monthly["active"] is True
    assert daily["active"] is False


def make_session(ip: str, time: datetime | None = None) -> IESession:
    return IESession(
        ip=ip,
        id="sess-1",
        time=time if time is not None else datetime(2026, 7, 20, 10, 30, 0),
        usage=5_000_000,
        location="ICT",
        is_current=False,
    )


def test_to_frontend_session_flags_the_calling_client() -> None:
    session = make_session("172.25.155.10")

    rendered = to_frontend_session(session, "172.25.155.10")

    assert rendered["is_current"] is True


def test_to_frontend_session_does_not_flag_other_clients() -> None:
    session = make_session("172.25.155.10")

    rendered = to_frontend_session(session, "172.25.155.11")

    assert rendered["is_current"] is False


def test_to_frontend_session_hides_tiny_usage() -> None:
    session = make_session("172.25.155.10")
    session.usage = 10

    assert to_frontend_session(session, "172.25.155.10")["usage"] == "-"


def test_to_frontend_session_tolerates_a_missing_start_time() -> None:
    session = make_session("172.25.155.10", time=None)
    session.time = None

    # acctstarttime is nullable, so rendering must not blow up on it.
    assert to_frontend_session(session, "172.25.155.10")["time"] == "-"
