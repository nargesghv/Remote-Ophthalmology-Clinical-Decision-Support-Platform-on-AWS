from __future__ import annotations


def validate_function_call(call: dict, schema: dict[str, list[str]]) -> list[str]:
    errors = []
    if call["name"] not in schema:
        errors.append("wrong_function_name")
        return errors

    required = schema.get(call["name"], [])
    for param in required:
        if param not in call["arguments"]:
            errors.append("missing_parameter")
    return errors
