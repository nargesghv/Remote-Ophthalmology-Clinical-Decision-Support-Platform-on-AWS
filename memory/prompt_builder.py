from __future__ import annotations

from pathlib import Path
from typing import Any

from memory.retrieve_feedback import build_query_record, retrieve_similar_feedback
from memory.feedback_memory import FeedbackMemoryStore


def load_prompt(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def build_summary_prompt_with_feedback(
    *,
    base_prompt_path: str,
    predicted_disease_label: str | None,
    predicted_action: str | None,
    notes: str,
    feedback_store: FeedbackMemoryStore,
    top_k: int = 2,
) -> str:
    base_prompt = load_prompt(base_prompt_path)
    query = build_query_record(
        predicted_disease_label=predicted_disease_label,
        predicted_action=predicted_action,
        notes=notes,
    )
    matches = retrieve_similar_feedback(
        query_record=query,
        store=feedback_store,
        top_k=top_k,
    )

    if not matches:
        return base_prompt

    fewshot = []
    for i, m in enumerate(matches, start=1):
        fewshot.append(
            f"Feedback Example {i}:\n"
            f"- predicted_disease_label: {m.get('predicted_disease_label')}\n"
            f"- corrected_disease_label: {m.get('corrected_disease_label')}\n"
            f"- predicted_action: {m.get('predicted_action')}\n"
            f"- corrected_action: {m.get('corrected_action')}\n"
            f"- issue: {m.get('summary_issue_type')}\n"
            f"- clinician_note: {m.get('notes')}\n"
        )

    return base_prompt + "\n\nRetrieved feedback guidance:\n\n" + "\n".join(fewshot)
