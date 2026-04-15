from __future__ import annotations


def evaluate_feedback_reuse(records: list[dict]) -> dict:
    total = len(records)
    reused = sum(1 for r in records if r.get("feedback_examples_used"))
    improved = sum(1 for r in records if r.get("feedback_examples_used") and r.get("improved"))
    return {
        "reuse_rate": reused / total if total else 0.0,
        "improvement_rate_given_reuse": improved / reused if reused else 0.0,
        "num_records": total,
    }
