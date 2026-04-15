from feedback_loop.retraining_trigger import should_trigger_retraining
from feedback_loop.champion_challenger import compare_models
from feedback_loop.rollback_promotion import decide_release_action


def test_retraining_trigger():
    assert should_trigger_retraining(
        override_rate=0.20,
        drift_score=0.25,
        new_feedback_count=25,
    ) is True


def test_champion_challenger():
    result = compare_models(
        {"accuracy": 0.80, "override_rate": 0.12, "groundedness_score": 0.88},
        {"accuracy": 0.84, "override_rate": 0.10, "groundedness_score": 0.90},
    )
    assert result["promote_challenger"] is True


def test_release_action():
    result = decide_release_action(promote_challenger=True, error_rate_spike=False, safety_violation=False)
    assert result["action"] == "promote"
