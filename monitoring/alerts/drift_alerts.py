def should_alert_drift(psi_score: float, threshold: float = 0.20) -> bool:
    return psi_score > threshold
