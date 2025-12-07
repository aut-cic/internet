from prometheus_client import Counter, Histogram

REQUEST_LATENCY = Histogram(
    name="request_latency_seconds",
    documentation="Description of histogram",
    labelnames=["view", "action"],
)

# define a counter metric
REQUEST_COUNTER = Counter(
    name="requests_total",
    documentation="Total number of requests received",
    labelnames=["view", "action"],
)
