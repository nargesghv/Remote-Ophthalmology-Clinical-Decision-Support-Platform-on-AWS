from prometheus_client import Counter, Gauge, Histogram

WORKFLOW_ACTION_COUNT = Counter(
    "workflow_action_total",
    "Count of workflow actions taken",
    ["action"],
)

URGENT_ESCALATIONS = Counter(
    "urgent_escalations_total",
    "Number of urgent clinician review cases",
)

RETAKE_REQUESTS = Counter(
    "retake_requests_total",
    "Number of retake requests",
)

WORKFLOW_SUCCESS = Counter(
    "workflow_success_total",
    "Completed workflow count",
    ["action"],
)

WORKFLOW_LATENCY = Histogram(
    "workflow_latency_seconds",
    "End-to-end workflow latency in seconds",
)

CLINICIAN_QUEUE_SIZE = Gauge(
    "clinician_review_queue_size",
    "Current clinician review queue size",
)
