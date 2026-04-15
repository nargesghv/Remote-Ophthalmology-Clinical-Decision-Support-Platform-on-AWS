from datetime import datetime, timezone

from memory.feedback_memory import FeedbackMemoryStore
from memory.memory_schema import FeedbackMemoryRecord
from memory.retrieve_feedback import build_query_record, retrieve_similar_feedback


def test_feedback_memory_retrieval(tmp_path):
    store = FeedbackMemoryStore(path=str(tmp_path / "feedback_memory.jsonl"))
    store.add(
        FeedbackMemoryRecord(
            case_id="case-1",
            patient_id="patient-1",
            predicted_disease_label="glaucoma",
            corrected_disease_label="glaucoma",
            predicted_action="standard_clinician_review",
            corrected_action="urgent_clinician_review",
            summary_issue_type="under_escalation",
            medication_conflict=False,
            notes="Urgent review needed for glaucoma suspicion.",
            doctor_id="doctor-1",
            timestamp=datetime.now(tz=timezone.utc).isoformat(),
        )
    )

    query = build_query_record(
        predicted_disease_label="glaucoma",
        predicted_action="standard_clinician_review",
        notes="under escalation issue",
    )
    matches = retrieve_similar_feedback(query_record=query, store=store, top_k=1)
    assert len(matches) == 1
    assert matches[0]["corrected_action"] == "urgent_clinician_review"
