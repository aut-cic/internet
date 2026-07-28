"""
Prometheus metrics shared by the HTTP views.

``PROMETHEUS_MULTIPROC_DIR`` has to be set *before* ``prometheus_client`` is
imported anywhere in the process: the library picks its value class at import
time, and without the variable it picks the in-process one. Every metric
defined here would then be invisible to the ``MultiProcessCollector`` that
serves ``/metrics``, so the endpoint would report nothing but per-process
defaults.

To keep that guarantee from depending on import order, this module is the only
one allowed to import ``prometheus_client`` -- everything else goes through
:func:`render_latest`. Hence the deliberately late import below.
"""

import os
from pathlib import Path

MULTIPROC_DIR = Path(os.environ.setdefault("PROMETHEUS_MULTIPROC_DIR", "./prom"))
MULTIPROC_DIR.mkdir(parents=True, exist_ok=True)

import prometheus_client  # noqa: E402
import prometheus_client.multiprocess  # noqa: E402

CONTENT_TYPE = prometheus_client.CONTENT_TYPE_LATEST

REQUEST_LATENCY = prometheus_client.Histogram(
    name="request_latency_seconds",
    documentation="Latency of handled requests in seconds",
    labelnames=["view", "action"],
)

REQUEST_COUNTER = prometheus_client.Counter(
    name="requests_total",
    documentation="Total number of requests received",
    labelnames=["view", "action"],
)


def render_latest() -> bytes:
    """
    Collect metrics from every uvicorn worker and render them for a scrape.
    """
    registry = prometheus_client.CollectorRegistry()
    prometheus_client.multiprocess.MultiProcessCollector(registry)
    return prometheus_client.generate_latest(registry)
