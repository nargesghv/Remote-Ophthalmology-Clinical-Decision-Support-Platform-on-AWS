from __future__ import annotations

from typing import Any

from memory.embed_feedback import embed_feedback_record
from memory.feedback_memory import FeedbackMemoryStore


def build_query_record(
    *,
    predicted_disease_label: str | None,
    predicted_action: str | None,
    notes: str = "",
) -> dict[str, Any]:
    return {
        "predicted_disease_label": predicted_disease_label,
        "predicted_action": predicted_action,
        "notes": notes,
    }


def retrieve_similar_feedback(
    *,
    query_record: dict[str, Any],
    store: FeedbackMemoryStore,
    top_k: int = 3,
) -> list[dict[str, Any]]:
    query_vec = embed_feedback_record(query_record)
    if not query_vec:
        return []

    scored = []
    for record in store.all():
        rec_vec = embed_feedback_record(record)
        overlap = len(query_vec.intersection(rec_vec))
        if overlap > 0:
            scored.append((overlap, record))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [record for _, record in scored[:top_k]]
