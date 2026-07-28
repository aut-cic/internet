"""
FastAPI application factory and configuration.
"""

import contextlib
import logging
from collections.abc import AsyncIterator

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqlalchemy.engine import Engine

from internet.announcements import announcements
from internet.http.site.view import router as site_router
from internet.http.status.view import router as status_router
from internet.http.system.view import router as system_router
from internet.model.urls import URLs
from internet.subnets import subnets

logger = logging.getLogger(__name__)


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """
    Report what the process loaded, then dispose of the pool on shutdown.
    """
    logger.info("loaded %d subnets", sum(1 for _ in subnets()))
    logger.info("loaded %d announcements", sum(1 for _ in announcements()))

    yield

    app.state.engine.dispose()


def create_app(urls: URLs, engine: Engine) -> FastAPI:
    """
    Create a FastAPI application and configure its dependencies.
    """
    app = FastAPI(title="Internet Usage System", lifespan=lifespan)

    app.state.engine = engine
    app.state.urls = urls

    # Mount static files BEFORE routers to prevent catch-all route from intercepting
    app.mount("/static", StaticFiles(directory="frontend/dist"), name="static")
    app.mount("/public", StaticFiles(directory="public"), name="public")

    # Router order matters: site_router owns a /{path:path} catch-all that
    # answers every path, so all other routers have to be included ahead of it.
    app.include_router(system_router)
    app.include_router(status_router)
    app.include_router(site_router)

    return app
