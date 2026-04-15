def should_alert_failure_rate(failure_rate: float, threshold: float = 0.05) -> bool:
    return failure_rate > threshold
