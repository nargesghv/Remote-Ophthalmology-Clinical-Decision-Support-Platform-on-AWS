from __future__ import annotations


def combine_findings(disease_result: dict, patient_background: dict, symptom_score: int) -> dict:
    reasons = []
    urgency = "routine"
    prescription_blocked = False

    if disease_result["severity"] == "high":
        urgency = "urgent"
        reasons.append("High severity disease classification")

    if "diabetes" in patient_background.get("conditions", []) and disease_result["disease_label"] == "diabetic_retinopathy":
        urgency = "standard"
        reasons.append("Relevant chronic condition found in patient background")

    if symptom_score >= 8:
        urgency = "urgent"
        reasons.append("High symptom score")

    if "penicillin" in patient_background.get("allergies", []):
        prescription_blocked = True
        reasons.append("Allergy requires manual prescription review")

    return {
        "urgency": urgency,
        "recommendation": "clinician_review_required",
        "prescription_blocked": prescription_blocked,
        "reasons": reasons,
        "reasoning_version": "reasoning_step2_v1",
    }
