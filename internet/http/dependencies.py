"""
FastAPI dependency injection for the application.

Everything is resolved from ``request.app.state``, which is populated by
:func:`internet.http.main.create_app`. Keeping it on the app instead of in
module-level globals is what lets the factory build more than one independent
app -- notably one per test.
"""

from collections.abc import Generator
from typing import Annotated

from fastapi import Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from internet.model.urls import URLs

# Template configuration - accessible by route modules
templates = Jinja2Templates(directory="templates")


def get_engine(request: Request) -> Engine:
    """Dependency to get the SQLAlchemy engine."""
    return request.app.state.engine


def get_urls(request: Request) -> URLs:
    """Dependency to get the URLs configuration."""
    return request.app.state.urls


def get_db_session(
    engine: Annotated[Engine, Depends(get_engine)],
) -> Generator[Session]:
    """Dependency to get a database session."""
    with Session(engine) as session:
        yield session


def get_client_ip(request: Request) -> str:
    """
    Get the client IP address.

    ``request.client`` already reflects the forwarded address because uvicorn
    runs with ``proxy_headers=True``; the header lookups below only matter for
    proxies it does not understand.
    """
    if request.client and request.client.host:
        return request.client.host

    x_real_ip = request.headers.get("x-real-ip")
    if x_real_ip:
        return x_real_ip

    cf_connecting_ip = request.headers.get("cf-connecting-ip")
    if cf_connecting_ip:
        return cf_connecting_ip

    return "127.0.0.1"


# Type aliases for cleaner dependency injection
EngineDep = Annotated[Engine, Depends(get_engine)]
URLsDep = Annotated[URLs, Depends(get_urls)]
ClientIPDep = Annotated[str, Depends(get_client_ip)]
DBSessionDep = Annotated[Session, Depends(get_db_session)]
