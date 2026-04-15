from __future__ import annotations

from serving.capture_inference import capture_inference


def local_disease_endpoint(payload: dict) -> dict:
    score = payload.get("symptom_score", 0)
    if score >= 8:
        result = {
            "disease_label": "glaucoma",
            "disease_name": "Glaucoma Suspicion",
            "severity": "high",
            "confidence": 0.88,
            "model_version": "disease_endpoint_step2_v1",
        }
    elif score >= 5:
        result = {
            "disease_label": "diabetic_retinopathy",
            "disease_name": "Diabetic Retinopathy",
            "severity": "medium",
            "confidence": 0.75,
            "model_version": "disease_endpoint_step2_v1",
        }
    else:
        result = {
            "disease_label": "normal",
            "disease_name": "No Major Abnormality Detected",
            "severity": "low",
            "confidence": 0.84,
            "model_version": "disease_endpoint_step2_v1",
        }

    capture_inference("disease_inference", {"payload_meta": {k: payload.get(k) for k in ("patient_id", "clinic_id", "symptom_score")}, "result": result})
    return result
