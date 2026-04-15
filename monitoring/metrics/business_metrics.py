from prometheus_client import Counter, Gauge, Histogram

CLINICIAN_OVERRIDE_COUNT = Counter(
    "clinician_override_total",
    "Number of clinician overrides"
)

CLINICIAN_APPROVAL_COUNT = Counter(
    "clinician_approval_total",
    "Number of clinician approvals"
)

CLINICIAN_REVIEW_TURNAROUND = Histogram(
    "clinician_review_turnaround_seconds",
    "Time from case creation to clinician decision"
)

OVERRIDE_RATE = Gauge(
    "override_rate",
    "Current clinician override rate"
)
