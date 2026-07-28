"""
Tests for AccountingService against a real (in-memory) database.
"""

from datetime import datetime

from sqlalchemy import Engine
from sqlalchemy.orm import Session

from internet.accounting.acct import AccountingService
from internet.accounting.usage import UsageType

from .conftest import CLIENT_IP, GROUP_NAME, USERNAME, make_account


def test_ip_to_username_finds_active_session(seeded_engine: Engine) -> None:
    with Session(seeded_engine) as session:
        assert AccountingService(session).ip_to_username(CLIENT_IP) == USERNAME


def test_ip_to_username_returns_none_for_unknown_ip(seeded_engine: Engine) -> None:
    with Session(seeded_engine) as session:
        assert AccountingService(session).ip_to_username("10.0.0.1") is None


def test_ip_to_username_ignores_closed_sessions(engine: Engine) -> None:
    with Session(engine) as session:
        session.add(
            make_account(ip="172.25.155.99", stop_time=datetime(2026, 7, 1, 12, 0, 0))
        )
        session.commit()

    with Session(engine) as session:
        # A session with a stop time is finished, so its IP maps to nobody.
        assert AccountingService(session).ip_to_username("172.25.155.99") is None


def test_user_usage_aggregates_windows(seeded_engine: Engine) -> None:
    with Session(seeded_engine) as session:
        report = AccountingService(session).user_usage(USERNAME)

    # Seeded discounted usage: 400 today, 200 three days ago, 50 ten days ago.
    assert report.usage.daily == 400
    assert report.usage.weekly == 600
    assert report.usage.monthly == 650
    # free mirrors the monthly total
    assert report.usage.free == 650


def test_user_usage_reports_discount_per_day(seeded_engine: Engine) -> None:
    with Session(seeded_engine) as session:
        report = AccountingService(session).user_usage(USERNAME)

    assert len(report.usage_history) == 3
    # discount is the gap between the raw and the discounted counter
    assert sorted(record.discount for record in report.usage_history) == [50, 100, 100]


def test_user_usage_resolves_group_and_package(seeded_engine: Engine) -> None:
    with Session(seeded_engine) as session:
        report = AccountingService(session).user_usage(USERNAME)

    assert report.groupname == GROUP_NAME
    assert report.package.daily_volume == 2
    assert report.package.weekly_volume == 10
    assert report.package.monthly_volume == 30
    # the free tier is derived, not stored
    assert report.package.free_volume == 4 * 30
    # "-H1" in the group name selects the weekly tier
    assert report.get_active_type() is UsageType.WEEKLY


def test_user_usage_lists_active_sessions_with_location(
    seeded_engine: Engine,
) -> None:
    with Session(seeded_engine) as session:
        report = AccountingService(session).user_usage(USERNAME)

    assert len(report.sessions) == 1
    active = report.sessions[0]
    assert active.ip == CLIENT_IP
    assert active.usage == 3_000_000
    # 172.25.155.0/24 is the ICT centre subnet
    assert active.location != "-"


def test_user_usage_handles_null_octet_counters(engine: Engine) -> None:
    with Session(engine) as session:
        session.add(make_account(input_octets=None, output_octets=None))
        session.commit()

    with Session(engine) as session:
        report = AccountingService(session).user_usage(USERNAME)

    # NULL counters must read as zero rather than raising.
    assert report.sessions[0].usage == 0


def test_user_usage_for_unknown_user_is_empty(seeded_engine: Engine) -> None:
    with Session(seeded_engine) as session:
        report = AccountingService(session).user_usage("nobody")

    assert report.usage_history == []
    assert report.sessions == []
    assert report.groupname == ""
    assert report.usage.monthly == 0
