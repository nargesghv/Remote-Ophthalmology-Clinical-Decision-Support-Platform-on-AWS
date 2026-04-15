from __future__ import annotations

from typing import Any

from app.config import settings


class MockQualityClient:
    def predict(self, payload: dict[str, Any]) -> dict[str, Any]:
        label = "good" if len(payload.get("image_b64", "")) > 40 else "bad"
        return {
            "label": label,
            "confidence": 0.93 if label == "good" else 0.55,
            "model_version": "quality_model_v1",
            "issues": [] if label == "good" else ["low_information_content"],
        }


class MockDiseaseClient:
    def predict(self, payload: dict[str, Any]) -> dict[str, Any]:
        score = payload.get("symptom_score", 0)
        if score >= 8:
            return {
                "disease_label": "glaucoma",
                "disease_name": "Glaucoma Suspicion",
                "severity": "high",
                "confidence": 0.88,
                "model_version": "disease_model_v1",
            }
        if score >= 5:
            return {
                "disease_label": "diabetic_retinopathy",
                "disease_name": "Diabetic Retinopathy",
                "severity": "medium",
                "confidence": 0.74,
                "model_version": "disease_model_v1",
            }
        return {
            "disease_label": "normal",
            "disease_name": "No Major Abnormality Detected",
            "severity": "low",
            "confidence": 0.82,
            "model_version": "disease_model_v1",
        }


def get_quality_client():
    if settings.use_mock_clients:
        return MockQualityClient()
    raise NotImplementedError("Real quality endpoint client not implemented in step 1 package.")


def get_disease_client():
    if settings.use_mock_clients:
        return MockDiseaseClient()
    raise NotImplementedError("Real disease endpoint client not implemented in step 1 package.")
