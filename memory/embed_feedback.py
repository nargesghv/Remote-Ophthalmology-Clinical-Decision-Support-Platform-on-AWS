from __future__ import annotations

from typing import Any


def embed_feedback_record(record: dict[str, Any]) -> set[str]:
    '''
    Very simple lexical embedding for demo purposes.
    In later steps this can be replaced with real embedding models.
    '''
    parts = [
        str(record.get("predicted_disease_label") or ""),
        str(record.get("corrected_disease_label") or ""),
        str(record.get("predicted_action") or ""),
        str(record.get("corrected_action") or ""),
        str(record.get("summary_issue_type") or ""),
        str(record.get("notes") or ""),
    ]
    tokens = " ".join(parts).lower().replace("_", " ").split()
    return set(t for t in tokens if t)
