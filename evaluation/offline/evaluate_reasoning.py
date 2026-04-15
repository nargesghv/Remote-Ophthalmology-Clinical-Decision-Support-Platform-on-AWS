from __future__ import annotations

from models.reasoning.multimodal_reasoning import combine_findings


def main():
    cases = [
        {
            "disease_result": {
                "disease_label": "glaucoma",
                "severity": "high",
                "confidence": 0.88,
            },
            "patient_background": {"conditions": [], "allergies": []},
            "symptom_score": 8,
            "expected_urgency": "urgent",
        },
        {
            "disease_result": {
                "disease_label": "normal",
                "severity": "low",
                "confidence": 0.82,
            },
            "patient_background": {"conditions": [], "allergies": []},
            "symptom_score": 1,
            "expected_urgency": "routine",
        },
    ]

    correct = 0
    for c in cases:
        result = combine_findings(c["disease_result"], c["patient_background"], c["symptom_score"])
        if result["urgency"] == c["expected_urgency"]:
            correct += 1

    print({"accuracy": correct / len(cases), "num_cases": len(cases)})


if __name__ == "__main__":
    main()
