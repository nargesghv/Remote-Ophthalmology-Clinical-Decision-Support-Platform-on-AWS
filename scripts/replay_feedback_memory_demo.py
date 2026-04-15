from datetime import datetime, timezone

from memory.feedback_memory import FeedbackMemoryStore
from memory.memory_schema import FeedbackMemoryRecord
from memory.retrieve_feedback import build_query_record, retrieve_similar_feedback


def main():
    store = FeedbackMemoryStore()

    store.add(
        FeedbackMemoryRecord(
            case_id="case-1",
            patient_id="patient-demo-1",
            predicted_disease_label="diabetic_retinopathy",
            corrected_disease_label="diabetic_retinopathy",
            predicted_action="routine_review",
            corrected_action="standard_clinician_review",
            summary_issue_type="missing_background_condition",
            medication_conflict=False,
            notes="Doctor said the summary must mention diabetes history and stronger review recommendation.",
            doctor_id="doctor-1",
            timestamp=datetime.now(tz=timezone.utc).isoformat(),
        )
    )

    store.add(
        FeedbackMemoryRecord(
            case_id="case-2",
            patient_id="patient-demo-2",
            predicted_disease_label="glaucoma",
            corrected_disease_label="glaucoma",
            predicted_action="standard_clinician_review",
            corrected_action="urgent_clinician_review",
            summary_issue_type="under_escalation",
            medication_conflict=False,
            notes="Urgent review needed for glaucoma suspicion.",
            doctor_id="doctor-2",
            timestamp=datetime.now(tz=timezone.utc).isoformat(),
        )
    )

    query = build_query_record(
        predicted_disease_label="diabetic_retinopathy",
        predicted_action="routine_review",
        notes="summary forgot chronic condition relevance",
    )

    matches = retrieve_similar_feedback(query_record=query, store=store, top_k=2)
    print("Retrieved matches:")
    for m in matches:
        print(m)


if __name__ == "__main__":
    main()
