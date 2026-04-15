from __future__ import annotations


def classify_error(errors: list[str]) -> str:
    if "wrong_function_name" in errors:
        return "FUNCTION_NAME_ERROR"
    if "missing_parameter" in errors:
        return "MISSING_PARAMETER"
    if "hallucinated_parameter" in errors:
        return "HALLUCINATED_PARAMETER"
    return "UNKNOWN_ERROR"
