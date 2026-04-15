from __future__ import annotations

from models.reasoning.multimodal_reasoning import combine_findings
from serving.capture_inference import capture_inference


def local_reasoning_endpoint(payload: dict) -> dict:
    result = combine_findings(
        disease_result=payload["disease_result"],
        patient_background=payload["patient_background"],
        symptom_score=payload["symptom_score"],
    )
    capture_inference("reasoning_inference", {"result": result})
    return result
