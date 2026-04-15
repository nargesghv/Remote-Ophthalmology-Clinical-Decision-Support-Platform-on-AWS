from prometheus_client import Counter, Histogram

SUMMARY_GENERATION_COUNT = Counter(
    "summary_generation_total",
    "Count of generated summaries"
)

SUMMARY_GENERATION_LATENCY = Histogram(
    "summary_generation_latency_seconds",
    "Latency of summary generation in seconds"
)

FALLBACK_USAGE_COUNT = Counter(
    "fallback_usage_total",
    "Number of times a fallback path was used",
    ["fallback_type"],
)

JUDGE_FAILURES = Counter(
    "judge_failures_total",
    "LLM judge failures"
)
