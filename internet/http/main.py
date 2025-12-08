"""
FastAPI application factory and configuration.
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqlalchemy.engine import Engine

from internet.http.dependencies import set_engine, set_urls
from internet.http.site.view import router as site_router
from internet.http.status.view import router as status_router
from internet.model.urls import URLs


def create_app(
    login_urls: dict[str, str], logout_urls: dict[str, str], engine: Engine
) -> FastAPI:
    """
    Create FastAPI application and configure dependencies.
    """
    app = FastAPI(title="Internet Usage System")

    # Set up dependency injection (replaces Sanic's app.ext.dependency)
    set_engine(engine)
    set_urls(URLs(login_urls, logout_urls))

    # Mount static files BEFORE routers to prevent catch-all route from intercepting
    app.mount("/static", StaticFiles(directory="frontend/dist"), name="static")
    app.mount("/public", StaticFiles(directory="public"), name="public")

    # Include routers (replaces Sanic's app.blueprint)
    # Note: status_router must come before site_router because site_router
    # has a catch-all route /{path:path} that would otherwise intercept /status
    app.include_router(status_router)
    app.include_router(site_router)

    return app
