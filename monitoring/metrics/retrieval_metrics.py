from prometheus_client import Counter, Gauge, Histogram

BACKGROUND_RETRIEVAL_LATENCY = Histogram(
    "background_retrieval_latency_seconds",
    "Patient background retrieval latency in seconds",
)

BACKGROUND_MISSING_RATE = Gauge(
    "background_missing_rate",
    "Rate of cases with missing patient background"
)

FEEDBACK_MEMORY_HITS = Counter(
    "feedback_memory_hits_total",
    "Total number of retrieved feedback examples"
)
