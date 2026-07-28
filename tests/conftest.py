"""
Shared fixtures.

The radius tables are plain SQLAlchemy models, so the whole accounting layer
can be exercised against an in-memory SQLite database -- no MySQL, no fixtures
on disk, and every test gets a clean schema.
"""

import atexit
import os
import shutil
import tempfile

# Point the metrics scratch directory somewhere disposable before anything
# imports internet.metrics, which reads the variable at import time. Otherwise
# the suite scribbles worker .db files into the repo's prom/ directory and
# those then show up in a locally served /metrics.
_METRICS_DIR = tempfile.mkdtemp(prefix="internet-metrics-")
os.environ["PROMETHEUS_MULTIPROC_DIR"] = _METRICS_DIR
atexit.register(shutil.rmtree, _METRICS_DIR, ignore_errors=True)

from collections.abc import Callable, Iterator  # noqa: E402
from datetime import datetime, timedelta  # noqa: E402

import pytest  # noqa: E402
from fastapi import FastAPI  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from sqlalchemy import Engine, create_engine  # noqa: E402
from sqlalchemy.orm import Session  # noqa: E402
from sqlalchemy.pool import StaticPool  # noqa: E402

from internet.http.main import create_app  # noqa: E402
from internet.model import Base  # noqa: E402
from internet.model.radacct import RadiusAccount  # noqa: E402
from internet.model.raddaily import RadiusDaily  # noqa: E402
from internet.model.radpackages import RadiusPackages  # noqa: E402
from internet.model.radusergroup import RadiusUserGroup  # noqa: E402
from internet.model.urls import URLs  # noqa: E402

USERNAME = "ali.rezaei"
GROUP_NAME = "students-H1"
CLIENT_IP = "172.25.155.10"


@pytest.fixture
def engine() -> Iterator[Engine]:
    # StaticPool keeps every checkout on the one connection that owns the
    # in-memory database, and check_same_thread=False lets TestClient's worker
    # thread reach it. Without both, the app would see an empty schema.
    eng = create_engine(
        "sqlite+pysqlite:///:memory:",
        poolclass=StaticPool,
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(eng)
    yield eng
    eng.dispose()


def make_account(
    username: str = USERNAME,
    ip: str = CLIENT_IP,
    unique_id: str = "sess-1",
    stop_time: datetime | None = None,
    input_octets: int | None = 1_000_000,
    output_octets: int | None = 2_000_000,
) -> RadiusAccount:
    """
    Build a radacct row with every NOT NULL column populated.
    """
    now = datetime(2026, 7, 20, 10, 30, 0)
    return RadiusAccount(
        account_session_id=unique_id,
        account_unique_id=unique_id,
        username=username,
        realm="aut.ac.ir",
        nas_ip_address="172.16.4.5",
        nas_port_id="1",
        nas_port_type="Ethernet",
        account_start_time=now,
        account_update_time=now,
        account_stop_time=stop_time,
        account_interval=60,
        account_session_time=3600,
        account_authentic="RADIUS",
        connectinfo_start="start",
        connectinfo_stop="stop",
        account_input_octets=input_octets,
        account_output_octets=output_octets,
        called_station_id="called",
        calling_station_id="calling",
        account_terminate_cause="",
        service_type="Login-User",
        framedprotocol="PPP",
        framedipaddress=ip,
    )


@pytest.fixture
def seeded_engine(engine: Engine) -> Engine:
    """
    An engine with one active session, a group, a package and 30 days of usage.
    """
    # Relative to now, because the accounting windows are computed from
    # datetime.now() -- fixed dates would silently drift out of range.
    today = datetime.now().date()
    with Session(engine) as session:
        session.add(make_account())
        session.add(
            RadiusUserGroup(username=USERNAME, group_name=GROUP_NAME, priority=1)
        )
        session.add(
            RadiusPackages(
                group_name="students",
                daily_volume=2,
                weekly_volume=10,
                monthly_volume=30,
                priority=1,
                session=1,
            )
        )
        # Three days of usage: today, 3 days ago, and 10 days ago. That spread
        # is what makes the daily/weekly/monthly windows distinguishable:
        # daily=400, weekly=600, monthly=650.
        for days_ago, original, discounted in (
            (0, 500, 400),
            (3, 300, 200),
            (10, 100, 50),
        ):
            session.add(
                RadiusDaily(
                    username=USERNAME,
                    usage_original=original,
                    usage_discount=discounted,
                    create_date=today - timedelta(days=days_ago),
                )
            )
        session.commit()
    return engine


@pytest.fixture
def urls() -> URLs:
    return URLs(
        login_urls={"1": "https://login.example.test/login"},
        logout_urls={"1": "http://logout.example.test:9090/logout"},
    )


@pytest.fixture
def app(seeded_engine: Engine, urls: URLs) -> FastAPI:
    return create_app(urls, seeded_engine)


@pytest.fixture
def client(app: FastAPI) -> Iterator[TestClient]:
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def client_from(app: FastAPI) -> Iterator[Callable[[str], TestClient]]:
    """
    Build a client that appears to connect from ``ip``.

    get_client_ip reads request.client first (uvicorn rewrites it from the
    proxy headers), so the source address has to be set on the ASGI scope --
    sending an x-real-ip header alone would be ignored.
    """
    opened: list[TestClient] = []

    def factory(ip: str) -> TestClient:
        test_client = TestClient(app, client=(ip, 12345))
        test_client.__enter__()
        opened.append(test_client)
        return test_client

    yield factory

    for test_client in opened:
        test_client.__exit__(None, None, None)
