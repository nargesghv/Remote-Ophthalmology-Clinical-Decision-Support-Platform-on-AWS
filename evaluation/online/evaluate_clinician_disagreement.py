from __future__ import annotations

from collections import defaultdict


def disagreement_by_clinic(records: list[dict]) -> dict:
    grouped = defaultdict(lambda: {"total": 0, "disagree": 0})
    for r in records:
        clinic = r["clinic_id"]
        grouped[clinic]["total"] += 1
        if r["ai_action"] != r["doctor_action"]:
            grouped[clinic]["disagree"] += 1

    return {
        clinic: {
            "override_rate": vals["disagree"] / vals["total"] if vals["total"] else 0.0,
            "total": vals["total"],
        }
        for clinic, vals in grouped.items()
    }
