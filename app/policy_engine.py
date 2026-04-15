from __future__ import annotations

from app.config import settings
from app.schemas import PolicyDecision


def decide_workflow_action(
    *,
    quality_label: str,
    quality_confidence: float,
    disease_label: str | None,
    disease_confidence: float | None,
    symptom_score: int,
    patient_background: dict | None,
) -> PolicyDecision:
    if quality_label != "good" or quality_confidence < settings.quality_pass_threshold:
        return PolicyDecision(
            action="request_retake",
            reason="Uploaded image quality is not sufficient for reliable interpretation.",
            priority="high",
            requires_human_review=False,
        )

    chronic = set((patient_background or {}).get("conditions", []))

    if disease_label in {"glaucoma", "retinal_detachment", "advanced_diabetic_retinopathy"}:
        return PolicyDecision(
            action="urgent_clinician_review",
            reason="High-risk disease class detected by specialist vision model.",
            priority="critical",
            requires_human_review=True,
        )

    if disease_confidence is not None and disease_confidence < settings.disease_confidence_threshold:
        return PolicyDecision(
            action="standard_clinician_review",
            reason="Prediction confidence below decision threshold; clinician validation required.",
            priority="high",
            requires_human_review=True,
        )

    if "diabetes" in chronic and disease_label == "diabetic_retinopathy":
        return PolicyDecision(
            action="standard_clinician_review",
            reason="Retinopathy signal with relevant patient history requires clinician review.",
            priority="high",
            requires_human_review=True,
        )

    if symptom_score >= 7:
        return PolicyDecision(
            action="standard_clinician_review",
            reason="High symptom severity requires clinician review even for non-critical image result.",
            priority="medium",
            requires_human_review=True,
        )

    return PolicyDecision(
        action="routine_review",
        reason="No urgent signal detected; case can proceed through routine clinician review.",
        priority="low",
        requires_human_review=True,
    )
