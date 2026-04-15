from __future__ import annotations

from typing import Any

from memory.feedback_memory import FeedbackMemoryStore


def build_gold_labels(store: FeedbackMemoryStore | None = None) -> list[dict[str, Any]]:
    store = store or FeedbackMemoryStore()
    gold = []
    for rec in store.all():
        gold.append(
            {
                "case_id": rec["case_id"],
                "patient_id": rec["patient_id"],
                "gold_disease_label": rec.get("corrected_disease_label") or rec.get("predicted_disease_label"),
                "gold_action": rec.get("corrected_action") or rec.get("predicted_action"),
                "notes": rec.get("notes", ""),
                "doctor_id": rec.get("doctor_id"),
            }
        )
    return gold


def main():
    labels = build_gold_labels()
    print({"num_gold_labels": len(labels), "labels": labels[:3]})


if __name__ == "__main__":
    main()
