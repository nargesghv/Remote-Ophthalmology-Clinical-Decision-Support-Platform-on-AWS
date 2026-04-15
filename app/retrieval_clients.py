from __future__ import annotations

from typing import Any

from app import db


class PatientBackgroundRetriever:
    def get_background(self, patient_id: str) -> dict[str, Any]:
        background = db.get_patient_background(patient_id)
        if background is None:
            return {
                "conditions": [],
                "medications": [],
                "allergies": [],
                "previous_diagnoses": [],
            }
        return background
