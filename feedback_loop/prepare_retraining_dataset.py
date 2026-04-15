from __future__ import annotations

from typing import Any

from feedback_loop.build_gold_labels import build_gold_labels


def prepare_retraining_dataset() -> list[dict[str, Any]]:
    labels = build_gold_labels()
    dataset = []
    for row in labels:
        dataset.append(
            {
                "case_id": row["case_id"],
                "patient_id": row["patient_id"],
                "target_disease_label": row["gold_disease_label"],
                "target_action": row["gold_action"],
                "notes": row["notes"],
            }
        )
    return dataset


def main():
    ds = prepare_retraining_dataset()
    print({"num_records": len(ds), "sample": ds[:3]})


if __name__ == "__main__":
    main()
