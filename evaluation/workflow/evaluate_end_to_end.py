from __future__ import annotations


def evaluate_end_to_end(cases: list[dict]) -> dict:
    total = len(cases)
    correct = sum(1 for c in cases if c["expected_action"] == c["predicted_action"])
    return {
        "num_cases": total,
        "routing_accuracy": correct / total if total else 0.0,
    }


def main():
    demo = [
        {"expected_action": "urgent_clinician_review", "predicted_action": "urgent_clinician_review"},
        {"expected_action": "routine_review", "predicted_action": "routine_review"},
        {"expected_action": "standard_clinician_review", "predicted_action": "routine_review"},
    ]
    print(evaluate_end_to_end(demo))


if __name__ == "__main__":
    main()
