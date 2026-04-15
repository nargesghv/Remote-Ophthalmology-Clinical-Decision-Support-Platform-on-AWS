from __future__ import annotations

import json
from pathlib import Path

import joblib
import numpy as np
from PIL import Image
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report


DATA_PATH = Path("data/synthetic/labels.jsonl")
MODEL_DIR = Path("artifacts/quality")
MODEL_DIR.mkdir(parents=True, exist_ok=True)


def extract_features(image_path: str) -> list[float]:
    img = Image.open(image_path).convert("L").resize((64, 64))
    arr = np.asarray(img, dtype=np.float32) / 255.0
    mean = float(arr.mean())
    std = float(arr.std())
    contrast = float(arr.max() - arr.min())
    return [mean, std, contrast]


def load_dataset():
    X, y = [], []
    with DATA_PATH.open("r", encoding="utf-8") as f:
        for line in f:
            row = json.loads(line)
            X.append(extract_features(row["image_path"]))
            y.append(int(row["quality_label"]))
    return np.array(X), np.array(y)


def main():
    X, y = load_dataset()
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    clf = LogisticRegression(max_iter=500)
    clf.fit(X_train, y_train)

    preds = clf.predict(X_test)
    report = classification_report(y_test, preds)
    print(report)

    joblib.dump(clf, MODEL_DIR / "quality_model.joblib")
    (MODEL_DIR / "metrics.txt").write_text(report, encoding="utf-8")
    print(f"Saved model to {MODEL_DIR / 'quality_model.joblib'}")


if __name__ == "__main__":
    main()
