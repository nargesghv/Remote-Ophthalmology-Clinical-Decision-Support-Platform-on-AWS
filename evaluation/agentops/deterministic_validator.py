from __future__ import annotations


def validate_action_schema(action: dict, allowed_actions: list[str]) -> dict:
    errors = {
        "valid_action_name": action.get("name") in allowed_actions,
        "missing_required_fields": [],
        "extra_fields": [],
    }
    required = ["name", "reason", "confidence"]
    for field in required:
        if field not in action:
            errors["missing_required_fields"].append(field)

    allowed_fields = set(required)
    for key in action.keys():
        if key not in allowed_fields:
            errors["extra_fields"].append(key)

    errors["schema_valid"] = (
        errors["valid_action_name"]
        and not errors["missing_required_fields"]
        and not errors["extra_fields"]
    )
    return errors
