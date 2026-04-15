from __future__ import annotations

from typing import Any


def compare_models(champion_metrics: dict[str, Any], challenger_metrics: dict[str, Any]) -> dict[str, Any]:
    challenger_better_accuracy = challenger_metrics.get("accuracy", 0.0) >= champion_metrics.get("accuracy", 0.0)
    challenger_safer_override = challenger_metrics.get("override_rate", 1.0) <= champion_metrics.get("override_rate", 1.0)
    challenger_better_grounding = challenger_metrics.get("groundedness_score", 0.0) >= champion_metrics.get("groundedness_score", 0.0)

    promote = challenger_better_accuracy and challenger_safer_override and challenger_better_grounding

    return {
        "promote_challenger": promote,
        "champion_metrics": champion_metrics,
        "challenger_metrics": challenger_metrics,
        "reason": (
            "Challenger meets or exceeds champion on accuracy, override rate, and grounding."
            if promote
            else "Keep champion; challenger did not meet promotion criteria."
        ),
    }


def main():
    champion = {"accuracy": 0.84, "override_rate": 0.10, "groundedness_score": 0.90}
    challenger = {"accuracy": 0.87, "override_rate": 0.09, "groundedness_score": 0.92}
    print(compare_models(champion, challenger))


if __name__ == "__main__":
    main()
