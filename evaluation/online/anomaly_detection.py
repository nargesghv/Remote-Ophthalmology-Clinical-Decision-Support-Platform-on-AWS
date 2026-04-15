from __future__ import annotations


def detect_override_spike(current_override_rate: float, threshold: float = 0.2) -> dict:
    return {
        "override_spike": current_override_rate > threshold,
        "current_override_rate": current_override_rate,
        "threshold": threshold,
    }
