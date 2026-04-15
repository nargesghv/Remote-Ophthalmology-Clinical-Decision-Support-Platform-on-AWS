from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class FeedbackMemoryRecord:
    case_id: str
    patient_id: str
    predicted_disease_label: Optional[str]
    corrected_disease_label: Optional[str]
    predicted_action: Optional[str]
    corrected_action: Optional[str]
    summary_issue_type: Optional[str]
    medication_conflict: bool
    notes: str
    doctor_id: str
    timestamp: str
    embedding_version: str = "simple-feedback-embed-v1"

    def to_dict(self) -> dict:
        return asdict(self)
