"""
FastAPI dependency injection for the application.
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

# Global state - set during app initialization
_engine: Engine | None = None
_urls: URLs | None = None


def set_engine(engine: Engine) -> None:
    """Set the SQLAlchemy engine for dependency injection."""
    global _engine
    _engine = engine


def set_urls(urls: URLs) -> None:
    """Set the URLs configuration for dependency injection."""
    global _urls
    _urls = urls


def get_engine() -> Engine:
    """Dependency to get SQLAlchemy engine."""
    if _engine is None:
        raise RuntimeError("Engine not initialized")
    return _engine


def get_urls() -> URLs:
    """Dependency to get URLs configuration."""
    if _urls is None:
        raise RuntimeError("URLs not initialized")
    return _urls


def get_db_session(
    engine: Annotated[Engine, Depends(get_engine)],
) -> Generator[Session]:
    """Dependency to get a database session."""
    with Session(engine) as session:
        yield session


def get_client_ip(request: Request) -> str:
    """
    Get client IP address, respecting X-Real-IP header for proxy setups.
    Equivalent to Sanic's request.remote_addr or request.ip
    """
    x_real_ip = request.headers.get("x-real-ip")
    if x_real_ip:
        return x_real_ip
    if request.client:
        return request.client.host
    return "127.0.0.1"


# Type aliases for cleaner dependency injection
EngineDep = Annotated[Engine, Depends(get_engine)]
URLsDep = Annotated[URLs, Depends(get_urls)]
ClientIPDep = Annotated[str, Depends(get_client_ip)]
DBSessionDep = Annotated[Session, Depends(get_db_session)]
