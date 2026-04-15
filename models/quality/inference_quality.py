from __future__ import annotations

import joblib
from pathlib import Path

from models.quality.train_quality_model import extract_features

MODEL_PATH = Path("artifacts/quality/quality_model.joblib")


def predict_quality(image_path: str) -> dict:
    clf = joblib.load(MODEL_PATH)
    feats = [extract_features(image_path)]
    pred = int(clf.predict(feats)[0])
    prob = float(clf.predict_proba(feats)[0][pred])
    return {
        "label": "good" if pred == 1 else "bad",
        "confidence": prob,
        "model_version": "quality_model_step2_v1",
    }
