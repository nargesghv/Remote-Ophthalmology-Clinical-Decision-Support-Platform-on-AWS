from __future__ import annotations

from memory.feedback_memory import FeedbackMemoryStore
from memory.retrieve_feedback import build_query_record, retrieve_similar_feedback


def main():
    store = FeedbackMemoryStore("data/feedback/feedback_memory.jsonl")
    query = build_query_record(
        predicted_disease_label="glaucoma",
        predicted_action="standard_clinician_review",
        notes="under escalation issue",
    )
    matches = retrieve_similar_feedback(query_record=query, store=store, top_k=3)
    print({"matches_found": len(matches), "matches": matches})


if __name__ == "__main__":
    main()
