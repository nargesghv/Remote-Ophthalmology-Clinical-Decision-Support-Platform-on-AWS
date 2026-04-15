def should_alert_override(override_rate: float, threshold: float = 0.15) -> bool:
    return override_rate > threshold
