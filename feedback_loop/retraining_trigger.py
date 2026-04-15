from __future__ import annotations


def should_trigger_retraining(
    *,
    override_rate: float,
    drift_score: float,
    new_feedback_count: int,
    override_threshold: float = 0.15,
    drift_threshold: float = 0.20,
    min_feedback_count: int = 20,
) -> bool:
    enough_feedback = new_feedback_count >= min_feedback_count
    quality_signal = override_rate > override_threshold or drift_score > drift_threshold
    return enough_feedback and quality_signal


def explain_retraining_decision(
    *,
    override_rate: float,
    drift_score: float,
    new_feedback_count: int,
) -> dict:
    decision = should_trigger_retraining(
        override_rate=override_rate,
        drift_score=drift_score,
        new_feedback_count=new_feedback_count,
    )
    return {
        "trigger_retraining": decision,
        "override_rate": override_rate,
        "drift_score": drift_score,
        "new_feedback_count": new_feedback_count,
    }
