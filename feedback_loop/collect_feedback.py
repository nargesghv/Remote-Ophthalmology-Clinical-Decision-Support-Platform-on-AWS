from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from memory.feedback_memory import FeedbackMemoryStore
from memory.memory_schema import FeedbackMemoryRecord


def _utc_now() -> str:
    return datetime.now(tz=timezone.utc).isoformat()


def build_feedback_record(
    *,
    case_id: str,
    patient_id: str,
    doctor_id: str,
    predicted_disease_label: str | None,
    corrected_disease_label: str | None,
    predicted_action: str | None,
    corrected_action: str | None,
    summary_issue_type: str | None,
    medication_conflict: bool,
    notes: str,
) -> FeedbackMemoryRecord:
    return FeedbackMemoryRecord(
        case_id=case_id,
        patient_id=patient_id,
        predicted_disease_label=predicted_disease_label,
        corrected_disease_label=corrected_disease_label,
        predicted_action=predicted_action,
        corrected_action=corrected_action,
        summary_issue_type=summary_issue_type,
        medication_conflict=medication_conflict,
        notes=notes,
        doctor_id=doctor_id,
        timestamp=_utc_now(),
    )


def store_feedback_record(record: FeedbackMemoryRecord, store: FeedbackMemoryStore | None = None) -> dict[str, Any]:
    store = store or FeedbackMemoryStore()
    store.add(record)
    return {
        "stored": True,
        "case_id": record.case_id,
        "doctor_id": record.doctor_id,
        "corrected_action": record.corrected_action,
    }
