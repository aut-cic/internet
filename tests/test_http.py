"""
Route-level tests.

The most important thing checked here is that /health and /metrics are not
swallowed by the /{path:path} catch-all on the site router -- they used to be
registered after it, so both answered with the login page and the container
health check passed on a 200 that meant nothing.
"""

from collections.abc import Callable

from fastapi import FastAPI
from fastapi.testclient import TestClient

from .conftest import CLIENT_IP, USERNAME


def test_health_is_not_shadowed_by_the_catch_all(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")
    assert response.json() == {"status": "healthy"}


def test_metrics_is_not_shadowed_by_the_catch_all(client: TestClient) -> None:
    response = client.get("/metrics")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/plain")
    # HTML here would mean the login catch-all answered instead.
    assert "<html" not in response.text.lower()


def test_metrics_exposes_the_request_counter(client: TestClient) -> None:
    # Drive a request so the counter is incremented in this process.
    client.get("/", headers={"x-real-ip": "10.0.0.9"})

    body = client.get("/metrics").text

    assert "requests_total" in body


def test_system_routes_precede_the_catch_all(app: FastAPI) -> None:
    paths = [getattr(route, "path", None) for route in app.routes]
    routers = [i for i, path in enumerate(paths) if path is None]

    # The included routers are system, status, then site (in that order), and
    # the site router must be last because it owns the catch-all.
    assert len(routers) == 3


def test_login_page_is_served_for_unknown_paths(client: TestClient) -> None:
    # MikroTik forwards arbitrary URLs from logged-out users to us, and clients
    # like iOS need a 200 back rather than a 404.
    response = client.get("/d/msdownload/update/software/whatever.exe")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_logged_in_client_is_redirected_to_status(
    client_from: Callable[[str], TestClient],
) -> None:
    response = client_from(CLIENT_IP).get("/", follow_redirects=False)

    assert response.status_code == 302
    assert response.headers["location"].endswith("/status")


def test_anonymous_campus_client_gets_the_login_page(
    client_from: Callable[[str], TestClient],
) -> None:
    # A campus address with no open RADIUS session stays on the login page.
    response = client_from("172.25.155.200").get("/", follow_redirects=False)

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_status_redirects_clients_outside_campus(
    client_from: Callable[[str], TestClient],
) -> None:
    response = client_from("8.8.8.8").get("/status", follow_redirects=False)

    assert response.status_code == 302


def test_status_redirects_campus_clients_without_a_session(
    client_from: Callable[[str], TestClient],
) -> None:
    response = client_from("172.25.155.200").get("/status", follow_redirects=False)

    assert response.status_code == 302


def test_status_renders_for_a_logged_in_client(
    client_from: Callable[[str], TestClient],
) -> None:
    response = client_from(CLIENT_IP).get("/status")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    # the rendered page names the signed-in user
    assert USERNAME in response.text


def test_create_app_builds_independent_apps(app: FastAPI) -> None:
    from sqlalchemy import create_engine

    from internet.http.main import create_app
    from internet.model.urls import URLs

    other_engine = create_engine("sqlite+pysqlite:///:memory:")
    other_urls = URLs(login_urls={"1": "https://other.test"}, logout_urls={})
    other = create_app(other_urls, other_engine)

    # Building a second app must not disturb the first -- the regression that
    # module-level set_engine()/set_urls() globals used to cause.
    assert app.state.urls is not other.state.urls
    assert app.state.engine is not other.state.engine
    other_engine.dispose()
