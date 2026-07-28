"""
Operational routes: liveness probe and Prometheus scrape endpoint.

These live on a router that is mounted before the site router, because the
site router owns a ``/{path:path}`` catch-all that would otherwise answer both
of them with the login page.
"""

from fastapi import APIRouter
from fastapi.responses import Response

from internet.metrics import CONTENT_TYPE, render_latest

router = APIRouter(tags=["system"])


@router.get("/health", name="health")
async def health() -> dict[str, str]:
    """
    Liveness probe used by the container HEALTHCHECK.
    """
    return {"status": "healthy"}


@router.get("/metrics", name="metrics")
async def metrics() -> Response:
    """
    Expose metrics collected across every uvicorn worker.
    """
    return Response(content=render_latest(), media_type=CONTENT_TYPE)
