from __future__ import annotations


def build_prescription_draft(disease_result: dict, reasoning_result: dict) -> dict:
    if reasoning_result.get("prescription_blocked"):
        return {
            "allowed": False,
            "draft": None,
            "reason": "Manual clinician prescription required due to allergy or safety rule.",
        }

    if disease_result["disease_label"] == "normal":
        return {
            "allowed": True,
            "draft": "No medication suggested. Routine follow-up recommended.",
            "reason": "No major abnormality detected.",
        }

    return {
        "allowed": True,
        "draft": f"Draft treatment suggestion for {disease_result['disease_name']} — clinician approval required.",
        "reason": "AI-generated draft only; not final medical advice.",
    }
