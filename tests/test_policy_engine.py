from app.policy_engine import decide_workflow_action


def test_policy_requests_retake_on_bad_quality():
    decision = decide_workflow_action(
        quality_label="bad",
        quality_confidence=0.4,
        disease_label=None,
        disease_confidence=None,
        symptom_score=2,
        patient_background=None,
    )
    assert decision.action == "request_retake"
