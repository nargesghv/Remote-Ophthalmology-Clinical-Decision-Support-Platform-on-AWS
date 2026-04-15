from __future__ import annotations

from typing import Any

from app import db
from app.schemas import FeedbackRequest


def record_feedback(case_id: str, feedback: FeedbackRequest) -> dict[str, Any]:
    payload = feedback.model_dump()
    db.save_clinician_feedback(case_id, feedback.doctor_id, payload)
    db.audit_event(case_id, "clinician_feedback_recorded", payload)
    return {
        "case_id": case_id,
        "stored": True,
        "approved": feedback.approved,
        "doctor_id": feedback.doctor_id,
    }
