from __future__ import annotations

from typing import Any


def build_structured_summary(
    *,
    quality_result: dict[str, Any],
    disease_result: dict[str, Any],
    patient_background: dict[str, Any],
    policy_decision: dict[str, Any],
    complaint: str | None,
) -> str:
    conditions = ", ".join(patient_background.get("conditions", [])) or "none reported"
    meds = ", ".join(patient_background.get("medications", [])) or "none reported"
    complaint_text = complaint if complaint else "No additional complaint provided."

    return (
        f"Clinical summary: Image quality was assessed as {quality_result['label']} "
        f"(confidence={quality_result['confidence']:.2f}). "
        f"Specialist vision inference suggests {disease_result['disease_name']} "
        f"(label={disease_result['disease_label']}, severity={disease_result['severity']}, "
        f"confidence={disease_result['confidence']:.2f}). "
        f"Relevant background includes conditions: {conditions}; medications: {meds}. "
        f"Patient complaint: {complaint_text}. "
        f"Recommended workflow action: {policy_decision['action']}. "
        f"Reason: {policy_decision['reason']}."
    )


def build_decision_explanation(
    *,
    quality_result: dict[str, Any],
    disease_result: dict[str, Any],
    patient_background: dict[str, Any],
    policy_decision: dict[str, Any],
) -> dict[str, Any]:
    return {
        "quality": quality_result,
        "disease": disease_result,
        "patient_background": patient_background,
        "policy": policy_decision,
    }
