from __future__ import annotations


def decide_release_action(*, promote_challenger: bool, error_rate_spike: bool, safety_violation: bool) -> dict:
    if safety_violation:
        return {"action": "rollback", "reason": "Safety violation detected."}
    if error_rate_spike:
        return {"action": "rollback", "reason": "Production error rate spike detected."}
    if promote_challenger:
        return {"action": "promote", "reason": "Challenger passed promotion criteria."}
    return {"action": "hold", "reason": "Insufficient evidence to promote challenger."}
