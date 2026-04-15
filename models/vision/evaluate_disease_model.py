from __future__ import annotations

import json
from pathlib import Path

import joblib
import numpy as np
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

from models.vision.train_disease_model import extract_features

DATA_PATH = Path("data/synthetic/labels.jsonl")
MODEL_PATH = Path("artifacts/vision/disease_model.joblib")


def main():
    clf = joblib.load(MODEL_PATH)
    X, y = [], []
    with DATA_PATH.open("r", encoding="utf-8") as f:
        for line in f:
            row = json.loads(line)
            X.append(extract_features(row["image_path"], row["age"], row["symptom_score"]))
            y.append(row["disease_label"])

    label_to_id = {"normal": 0, "diabetic_retinopathy": 1, "glaucoma": 2}
    y_ids = np.array([label_to_id[v] for v in y])
    X = np.array(X)
    preds = clf.predict(X)

    print("accuracy:", accuracy_score(y_ids, preds))
    print("confusion_matrix:", confusion_matrix(y_ids, preds))
    print(classification_report(y_ids, preds))


if __name__ == "__main__":
    main()
