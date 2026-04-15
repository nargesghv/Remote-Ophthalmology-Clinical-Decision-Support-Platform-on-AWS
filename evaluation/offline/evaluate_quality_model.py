from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

LABELS_PATH = Path("data/synthetic/labels.jsonl")


def evaluate_quality_predictions(predictions: list[int], labels: list[int]) -> dict:
    return {
        "accuracy": float(accuracy_score(labels, predictions)),
        "confusion_matrix": confusion_matrix(labels, predictions).tolist(),
        "classification_report": classification_report(labels, predictions, output_dict=True),
    }


def main():
    labels = []
    preds = []
    with LABELS_PATH.open("r", encoding="utf-8") as f:
        for line in f:
            row = json.loads(line)
            labels.append(int(row["quality_label"]))
            preds.append(int(row["quality_label"]))  # demo perfect baseline

    result = evaluate_quality_predictions(preds, labels)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
