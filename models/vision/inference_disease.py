from __future__ import annotations

from pathlib import Path
import joblib

from models.vision.train_disease_model import extract_features

MODEL_PATH = Path("artifacts/vision/disease_model.joblib")
ID_TO_RESULT = {
    0: ("normal", "No Major Abnormality Detected", "low"),
    1: ("diabetic_retinopathy", "Diabetic Retinopathy", "medium"),
    2: ("glaucoma", "Glaucoma Suspicion", "high"),
}


def predict_disease(image_path: str, age: int, symptom_score: int) -> dict:
    clf = joblib.load(MODEL_PATH)
    feats = [extract_features(image_path, age, symptom_score)]
    pred = int(clf.predict(feats)[0])
    prob = float(clf.predict_proba(feats)[0][pred])
    label, name, severity = ID_TO_RESULT[pred]
    return {
        "disease_label": label,
        "disease_name": name,
        "severity": severity,
        "confidence": prob,
        "model_version": "disease_model_step2_v1",
    }
