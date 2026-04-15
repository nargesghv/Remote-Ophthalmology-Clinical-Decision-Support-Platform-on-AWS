from __future__ import annotations

import json
from pathlib import Path

import joblib
import numpy as np
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

from models.quality.train_quality_model import extract_features

DATA_PATH = Path("data/synthetic/labels.jsonl")
MODEL_PATH = Path("artifacts/quality/quality_model.joblib")


def main():
    clf = joblib.load(MODEL_PATH)
    X, y = [], []
    with DATA_PATH.open("r", encoding="utf-8") as f:
        for line in f:
            row = json.loads(line)
            X.append(extract_features(row["image_path"]))
            y.append(int(row["quality_label"]))

    X = np.array(X)
    y = np.array(y)
    preds = clf.predict(X)

    print("accuracy:", accuracy_score(y, preds))
    print("confusion_matrix:", confusion_matrix(y, preds))
    print(classification_report(y, preds))


if __name__ == "__main__":
    main()
