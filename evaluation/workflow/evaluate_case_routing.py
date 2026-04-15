from __future__ import annotations


def evaluate_case_routing(records: list[dict]) -> dict:
    total = len(records)
    correct = sum(1 for r in records if r["expected_action"] == r["predicted_action"])
    urgent_missed = sum(
        1 for r in records
        if r["expected_action"] == "urgent_clinician_review" and r["predicted_action"] != "urgent_clinician_review"
    )
    return {
        "routing_accuracy": correct / total if total else 0.0,
        "urgent_missed": urgent_missed,
        "num_cases": total,
    }


def main():
    demo = [
        {"expected_action": "urgent_clinician_review", "predicted_action": "standard_clinician_review"},
        {"expected_action": "routine_review", "predicted_action": "routine_review"},
    ]
    print(evaluate_case_routing(demo))


if __name__ == "__main__":
    main()
