from __future__ import annotations


def evaluate_background_retrieval(retrieved: dict, expected_keys: list[str]) -> dict:
    present = sum(1 for key in expected_keys if key in retrieved)
    return {
        "expected_keys": expected_keys,
        "present_keys": present,
        "completeness": present / len(expected_keys) if expected_keys else 1.0,
    }


def main():
    retrieved = {
        "conditions": ["diabetes"],
        "medications": ["metformin"],
        "allergies": ["penicillin"],
    }
    print(evaluate_background_retrieval(retrieved, ["conditions", "medications", "allergies", "previous_diagnoses"]))


if __name__ == "__main__":
    main()
