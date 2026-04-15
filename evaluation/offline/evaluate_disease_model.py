from __future__ import annotations

import json
from pathlib import Path

from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

LABELS_PATH = Path("data/synthetic/labels.jsonl")
LABEL_TO_ID = {"normal": 0, "diabetic_retinopathy": 1, "glaucoma": 2}


def main():
    labels = []
    preds = []
    with LABELS_PATH.open("r", encoding="utf-8") as f:
        for line in f:
            row = json.loads(line)
            true_id = LABEL_TO_ID[row["disease_label"]]
            labels.append(true_id)
            preds.append(true_id)  # demo perfect baseline

    result = {
        "accuracy": float(accuracy_score(labels, preds)),
        "confusion_matrix": confusion_matrix(labels, preds).tolist(),
        "classification_report": classification_report(labels, preds, output_dict=True),
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
