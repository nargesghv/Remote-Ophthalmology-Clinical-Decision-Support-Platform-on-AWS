def should_alert_latency(p95_latency_seconds: float, threshold: float = 2.0) -> bool:
    return p95_latency_seconds > threshold
