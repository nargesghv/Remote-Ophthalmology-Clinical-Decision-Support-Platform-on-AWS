from __future__ import annotations


def evaluate_human_override(records: list[dict]) -> dict:
    total = len(records)
    overrides = sum(1 for r in records if r["ai_action"] != r["doctor_action"])
    return {
        "total_cases": total,
        "override_rate": overrides / total if total else 0.0,
        "agreement_rate": (total - overrides) / total if total else 0.0,
    }


def main():
    demo = [
        {"ai_action": "routine_review", "doctor_action": "standard_clinician_review"},
        {"ai_action": "urgent_clinician_review", "doctor_action": "urgent_clinician_review"},
    ]
    print(evaluate_human_override(demo))


if __name__ == "__main__":
    main()
