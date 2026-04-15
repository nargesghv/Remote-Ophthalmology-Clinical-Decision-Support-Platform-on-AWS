from __future__ import annotations

from models.reasoning.multimodal_reasoning import combine_findings


def main():
    disease_result = {
        "disease_label": "diabetic_retinopathy",
        "disease_name": "Diabetic Retinopathy",
        "severity": "medium",
        "confidence": 0.8,
    }
    patient_background = {
        "conditions": ["diabetes"],
        "allergies": ["penicillin"],
        "medications": ["metformin"],
    }
    result = combine_findings(disease_result, patient_background, symptom_score=8)
    print(result)


if __name__ == "__main__":
    main()
