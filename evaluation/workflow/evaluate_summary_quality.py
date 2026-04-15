from __future__ import annotations


def deterministic_summary_check(summary: str, required_phrases: list[str]) -> dict:
    missing = [p for p in required_phrases if p.lower() not in summary.lower()]
    return {
        "all_required_present": len(missing) == 0,
        "missing_phrases": missing,
    }


def main():
    summary = "Clinical summary: Image quality was assessed as good. Specialist vision inference suggests Glaucoma Suspicion."
    print(deterministic_summary_check(summary, ["image quality", "glaucoma", "recommended workflow action"]))


if __name__ == "__main__":
    main()
