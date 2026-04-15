from __future__ import annotations


def build_scorecard(*, routing_accuracy: float, groundedness_score: float, override_rate: float) -> dict:
    return {
        "routing_accuracy": routing_accuracy,
        "groundedness_score": groundedness_score,
        "override_rate": override_rate,
        "overall_status": "good" if routing_accuracy >= 0.8 and override_rate <= 0.2 else "needs_attention",
    }
