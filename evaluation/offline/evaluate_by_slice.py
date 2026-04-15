from __future__ import annotations

from collections import defaultdict


def evaluate_by_slice(records: list[dict], slice_key: str, label_key: str, pred_key: str) -> dict:
    grouped = defaultdict(list)
    for r in records:
        grouped[r[slice_key]].append(r)

    output = {}
    for slice_value, items in grouped.items():
        total = len(items)
        correct = sum(1 for x in items if x[label_key] == x[pred_key])
        output[slice_value] = {"accuracy": correct / total if total else 0.0, "count": total}
    return output


def main():
    demo = [
        {"clinic_id": "a", "label": "normal", "pred": "normal"},
        {"clinic_id": "a", "label": "glaucoma", "pred": "glaucoma"},
        {"clinic_id": "b", "label": "normal", "pred": "glaucoma"},
    ]
    print(evaluate_by_slice(demo, "clinic_id", "label", "pred"))


if __name__ == "__main__":
    main()
